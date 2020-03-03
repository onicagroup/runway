"""CFNgin entrypoint."""
import logging
import os
import re
import sys

from yaml.constructor import ConstructorError

from runway.util import AWS_ENV_VARS, MutableMap, cached_property

from .actions import build, destroy, diff
from .config import render_parse_load as load_config
from .context import Context as CFNginContext
from .environment import parse_environment
from .providers.aws.default import ProviderBuilder

# explicitly name logger so its not redundant
LOGGER = logging.getLogger('runway.cfngin')


class CFNgin(object):
    """Control CFNgin.

    Attributes:
        EXCLUDE_REGEX (str): Regex used to exclude YAML files when searching
            for config files.
        EXCLUDE_LIST (str): Global list of YAML file names to exclude when
            searching for config files.
        concurrency (int): Max number of CFNgin stacks that can be deployed
            concurrently. If the value is ``0``, will be constrained based on
            the underlying graph.
        interactive (bool): Wether or not to prompt the user before taking
            action.
        parameters (MutableMap): Combination of the parameters provided when
            initalizing the class and any environment files that are found.
        recreate_failed (bool): Destroy and re-create stacks that are stuck in
            a failed state from an initial deployment when updating.
        region (str): The AWS region where CFNgin is currently being executed.
        sys_path (str): Working directory.
        tail (bool): Wether or not to display all CloudFormation events in the
            terminal.

    """

    EXCLUDE_REGEX = r'runway(\..*)?\.(yml|yaml)'
    EXCLUDE_LIST = ['buildspec.yml', 'docker-compose.yml']

    def __init__(self, ctx, parameters=None, sys_path=None):
        """Instantiate class.

        Args:
            ctx (runway.context.Context): Runway context object.
            parameters (Optional[Dict[str. Any]]): Parameters from Runway.
            sys_path (Optional[str]): Working directory.

        """
        self.__ctx = ctx
        self._aws_credential_backup = {}
        self._env_file_name = None
        self.concurrency = ctx.max_concurrent_cfngin_stacks
        self.interactive = ctx.is_interactive
        self.parameters = MutableMap()
        self.recreate_failed = ctx.is_noninteractive
        self.region = ctx.env_region
        self.sys_path = sys_path or os.getcwd()
        self.tail = ctx.debug

        self.parameters.update(self.env_file)

        if parameters:
            LOGGER.debug('Adding Runway parameters to CFNgin parameters')
            self.parameters.update(parameters)

        self._inject_common_parameters()
        self._save_aws_credentials()

    @cached_property
    def env_file(self):
        """Contents of a CFNgin environment file.

        Returns:
            MutableMap

        """
        result = {}
        supported_names = ['{}.env'.format(self.__ctx.env_name),
                           '{}-{}.env'.format(self.__ctx.env_name,
                                              self.region)]
        for _, file_name in enumerate(supported_names):
            file_path = os.path.join(self.sys_path, file_name)
            if os.path.isfile(file_path):
                LOGGER.info('Found environment file: %s', file_path)
                self._env_file_name = file_path
                with open(file_path, 'r') as file_:
                    result.update(parse_environment(file_.read()))
        return MutableMap(**result)

    def deploy(self, sys_path=None):
        """Run the CFNgin deploy action.

        Args:
            syspath (Optional[str]): Explicitly define a path to work in.
                If not provided, ``self.sys_path`` is used.

        """
        self._inject_aws_credentials()
        if not sys_path:
            sys_path = self.sys_path
        config_files = self.find_config_files(sys_path=sys_path)

        for config in config_files:
            ctx = self.load(config)
            LOGGER.info('%s: deploying...', os.path.basename(config))
            action = build.Action(
                context=ctx,
                provider_builder=self._get_provider_builder(
                    ctx.config.service_role
                )
            )
            action.execute(concurrency=self.concurrency,
                           tail=self.tail)
        self._restore_aws_credentials()

    def destroy(self, sys_path=None):
        """Run the CFNgin destroy action.

        Args:
            syspath (Optional[str]): Explicitly define a path to work in.
                If not provided, ``self.sys_path`` is used.

        """
        self._inject_aws_credentials()
        if not sys_path:
            sys_path = self.sys_path
        config_files = self.find_config_files(sys_path=sys_path)
        # destroy should run in reverse to handle dependencies
        config_files.reverse()

        for config in config_files:
            ctx = self.load(config)
            LOGGER.info('%s: destroying...', os.path.basename(config))
            action = destroy.Action(
                context=ctx,
                provider_builder=self._get_provider_builder(
                    ctx.config.service_role
                )
            )
            action.execute(concurrency=self.concurrency,
                           force=True,
                           tail=self.tail)
        self._restore_aws_credentials()

    def load(self, config_path):
        """Load a CFNgin config into a context object.

        Args:
            config_path (str): Valid path to a CFNgin config file.

        Returns:
            :class:`runway.cfngin.context.Context`

        """
        LOGGER.debug('%s: loading...', os.path.basename(config_path))
        try:
            config = self._get_config(config_path)
            context = self._get_context(config)
            return context
        except ConstructorError as err:
            if err.problem.startswith('could not determine a constructor '
                                      'for the tag \'!'):
                LOGGER.error('"%s" appears to be a CloudFormation template, '
                             'but is located in the top level of a module '
                             'alongside the CloudFormation config files (i.e. '
                             'the file or files indicating the stack names & '
                             'parameters). Please move the template to a '
                             'subdirectory.', config_path)
                sys.exit(1)
            raise

    def plan(self, sys_path=None):
        """Run the CFNgin plan action.

        Args:
            syspath (Optional[str]): Explicitly define a path to work in.
                If not provided, ``self.sys_path`` is used.

        """
        self._inject_aws_credentials()
        if not sys_path:
            sys_path = self.sys_path
        config_files = self.find_config_files(sys_path=sys_path)
        for config in config_files:
            ctx = self.load(config)
            LOGGER.info('%s: generating change sets...',
                        os.path.basename(config))
            action = diff.Action(
                context=ctx,
                provider_builder=self._get_provider_builder(
                    ctx.config.service_role
                )
            )
            action.execute()
        self._restore_aws_credentials()

    def _get_config(self, file_path, validate=True):
        """Initialize a CFNgin config object from a file.

        Args:
            file_path (str): Path to the config file to load.
            validate (bool): Validate the loaded config.

        Returns:
            :class:`runway.cfngin.config.Config`

        """
        with open(file_path, 'r') as file_:
            raw_config = file_.read()
        return load_config(raw_config, self.parameters, validate)

    def _get_context(self, config):
        """Initialize a CFNgin context object.

        Args:
            config (:class:`runway.cfngin.config.Config): CFNgin config object.

        Returns:
            :class:`runway.cfngin.context.Context`

        """
        return CFNginContext(
            config=config,
            environment=self.parameters,
            force_stacks=[],  # placeholder
            region=self.region,
            stack_names=[]  # placeholder
        )

    def _get_provider_builder(self, service_role=None):
        """Initialize provider builder.

        Args:
            service_role (Optional[str]): CloudFormation service role.

        Returns:
            ProviderBuilder

        """
        if self.interactive:
            LOGGER.info('Using interactive AWS provider mode.')
        else:
            LOGGER.info('Using default AWS provider mode.')
        return ProviderBuilder(
            interactive=self.interactive,
            recreate_failed=self.recreate_failed,
            region=self.region,
            service_role=service_role
        )

    # TODO remove after deprecated `get_session` is removed
    def _inject_aws_credentials(self):
        """Change environment AWS credentials."""
        LOGGER.debug('Injecting AWS credentials into the environment before '
                     'running a CFNgin action')
        os.environ.update(self.__ctx.current_aws_creds)

    def _inject_common_parameters(self):
        """Add common parameters if they don't already exist.

        Adding these commonly used parameters will remove the need to add
        lookup support (mainly for environment variable lookups) in places
        such as ``cfngin_bucket``.

        Injected Parameters
        ~~~~~~~~~~~~~~~~~~~

        **environment (str)**
            Taken from the ``DEPLOY_ENVIRONMENT`` environment variable. This
            will the be current Runway environment being processed.

        **region (str)**
            Taken from the ``AWS_REGION`` environment variable. This will be
            the current region being deployed to.

        """
        if not self.parameters.get('environment'):
            self.parameters['environment'] = self.__ctx.env_name
        if not self.parameters.get('region'):
            self.parameters['region'] = self.region

    # TODO remove after deprecated `get_session` is removed
    def _save_aws_credentials(self):
        """Save a copy of existing AWS credentials from the environment."""
        LOGGER.debug('Creating a backup of AWS credentials from the '
                     'environment before running CFNgin')
        temp = os.environ.copy()
        for name in AWS_ENV_VARS:
            value = temp.get(name)
            if value:
                self._aws_credential_backup[name] = value

    # TODO remove after deprecated `get_session` is removed
    def _restore_aws_credentials(self):
        """Restore original AWS credentials to the environment."""
        LOGGER.debug('Restoring AWS credential backup post CFNgin action')
        for name in AWS_ENV_VARS:
            value = self._aws_credential_backup.get(name)
            if value:
                os.environ[name] = value
            else:
                # remove key if it exists, no error raised if it doesn't
                os.environ.pop(name, None)

    @classmethod
    def find_config_files(cls, exclude=None, sys_path=None):
        """Find CFNgin config files.

        Args:
            exclude (Optional[List[str]]): List of file names to exclude. This
                list is appended to the global exclude list.
            sys_path (Optional[str]): Explicitly define a path to search for
                config files.

        Returns:
            List[str]: Path to config files that were found.

        """
        if not sys_path:
            sys_path = os.getcwd()
        elif os.path.isfile(sys_path):
            return [sys_path]

        exclude = exclude or []
        result = []
        exclude.extend(cls.EXCLUDE_LIST)
        for root, _dirs, files in os.walk(sys_path):
            for name in files:
                if re.match(cls.EXCLUDE_REGEX, name) or (name in exclude or
                                                         name.startswith('.')):
                    # Hidden files (e.g. .gitlab-ci.yml), Runway configs,
                    # and docker-compose files definitely aren't stacker
                    # config files
                    continue
                if os.path.splitext(name)[-1] in ['.yaml', '.yml']:
                    result.append(os.path.join(root, name))
            break  # only need top level files
        result.sort()
        return result
