"""Runway config file module."""
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union, Iterator  # pylint: disable=unused-import
import yaml

LOGGER = logging.getLogger('runway')


class ConfigComponent(object):
    """Base class for Runway config components."""

    def get(self, key, default=None):
        # type: (str, Any) -> Any
        """Implement evaluation of get."""
        return getattr(self, key, getattr(self, key.replace('-', '_'), default))

    def __getitem__(self, key):
        # type: (str) -> Any
        """Implement evaluation of self[key]."""
        return getattr(self, key, getattr(self, key.replace('-', '_')))

    def __setitem__(self, key, value):
        # type: (str, Any) -> None
        """Implement evaluation of self[key] for assignment."""
        setattr(self, key, value)

    def __len__(self):
        # type: () -> int
        """Implement the built-in function len()."""
        return len(self.__dict__)

    def __iter__(self):
        # type: () -> Iterator[Any]
        """Return iterator object that can iterate over all attributes."""
        return iter(self.__dict__)


class ModuleDefinition(ConfigComponent):
    """A module defines the directory to be processed and applicable options.

    It can consist of `CloudFormation`_ (using `Stacker`_),
    `Troposphere`_ (using `Stacker`_), `Terraform`_,
    `Serverless Framework`_, or `AWS CDK`_. Each directory should end
    with their corresponding suffix for identification but, this is not
    required. See :ref:`Repo Structure<repo-structure>` for examples of
    a module directory structure.

    +------------------+-----------------------------------------------+
    | Suffix/Extension | IaC Tool/Framework                            |
    +==================+===============================================+
    | ``.cdk``         | `AWS CDK`_                                    |
    +------------------+-----------------------------------------------+
    | ``.cfn``         | `CloudFormation`_, `Troposphere`_ (`Stacker`_)|
    +------------------+-----------------------------------------------+
    | ``.sls``         | `Serverless Framework`_                       |
    +------------------+-----------------------------------------------+
    | ``.tf``          | `Terraform`_                                  |
    +------------------+-----------------------------------------------+

    A module is only deployed if there is a corresponding env/config
    present. This can take the form of either a file in the module folder
    or the ``environments`` option being defined. The naming format
    varies per-module type. See
    :ref:`Module Configurations<module-configurations>` for acceptable
    env/config file name formats.

    Modules can be defined as a string or a mapping. The minimum
    requirement for a module is a string that is equal to the name of
    the module directory. Providing a string is the same as providing a
    value for ``path`` in a mapping definition.

    Example:
      .. code-block:: yaml

        deployments:
          - modules:
              - my-module.cfn  # this
              - path: my-module.cfn  # is the same as this

    Using a map to define a module provides the ability to specify
    per-module ``options``, environment values, tags, and even a custom
    class for processing the module. The options that can be used with
    each module vary. For detailed information about module-specific
    options, see :ref:`Module Configurations<module-configurations>`.

    Example:
      .. code-block:: yaml

        deployments:
          - modules:
              - name: my-module
                path: my-module.tf
                environments:
                  dev:
                    image_id: ami-1234
                tags:
                  - app:example
                  - my-tag
                options:
                  terraform_backend_config:
                    region: us-east-1
                  terraform_backend_cfn_outputs:
                    bucket: StackName::OutputName
                    dynamodb_table: StackName::OutputName

    """

    def __init__(self,  # pylint: disable=too-many-arguments
                 name,  # type: str
                 path,  # type: str
                 class_path=None,  # type: Optional[str]
                 environments=None,  # type: Optional[Dict[str, Dict[str, Any]]]
                 options=None,  # type: Optional[Dict[str, Any]]
                 tags=None  # type: Optional[Dict[str, str]]
                 # pylint only complains for python2
                 ):  # pylint: disable=bad-continuation
        # type: (...) -> None
        """.. Runway module definition.

        Keyword Args:
            name (str): Name of the module. Used to more easily identify
                where different modules begin/end in the logs.
            path (str): Path to the module relative to the Runway config
                file. This cannot be higher than the Runway config file.
            class_path (Optional[str]): Path to custom Runway module class.
                Also used for static site deployments. See
                :ref:`Module Configurations<module-configurations>` for
                detailed usage.
            environments (Optional[Dict[str, Dict[str, Any]]]): Mapping for
                variables to environment names. When run, the variables
                defined here are merged with those in the
                ``.env``/``.tfenv``/environment config file. If this is
                defined, ``.env`` files can be omitted and the module
                will still be processed.
            options (Optional[Dict[str, Any]]): Module-specific options.
                See :ref:`Module Configurations<module-configurations>`
                for detailed usage.
            tags (Optional[Dict[str, str]]): Module tags used to select
                which modules to process using CLI arguments.
                (``--tag <tag>...``)

        References:
            - `AWS CDK`_
            - `CloudFormation`_
            - `Serverless Framework`_
            - `Stacker`_
            - `Troposphere`_
            - `Terraform`_
            - :ref:`Module Configurations<module-configurations>` -
              detailed module ``options``
            - :ref:`Repo Structure<repo-structure>` - examples of
              directory structure
            - :ref:`command-deploy`
            - :ref:`command-destroy`
            - :ref:`command-plan`

        """
        self.name = name
        self.path = path
        self.class_path = class_path
        self.environments = environments or {}
        self.options = options or {}
        self.tags = tags or {}

    @classmethod
    def from_list(cls, modules):
        """Instantiate ModuleDefinition from a list."""
        results = []
        for mod in modules:
            if isinstance(mod, str):
                results.append(cls(mod, mod, {}))
                continue
            name = mod.pop('name', mod['path'])
            results.append(cls(name,
                               mod.pop('path'),
                               class_path=mod.pop('class_path', None),
                               environments=mod.pop('environments', {}),
                               options=mod.pop('options', {}),
                               tags=mod.pop('tags', {})))

            if mod:
                LOGGER.warning(
                    'Invalid keys found in module %s have been ignored: %s',
                    name, ', '.join(mod.keys())
                )
        return results


class DeploymentDefinition(ConfigComponent):  # pylint: disable=too-many-instance-attributes
    """A deployment defines modules and options that affect the modules.

    Deployments are processed during a ``deploy``/``destroy``/``plan``
    action. If the processing of one deployment fails, the action will
    end.

    During a ``deploy``/``destroy`` action, the user has the option to
    select which deployment will run unless the ``CI`` environment
    variable is set, the ``--tag <tag>...`` cli option was provided, or
    only one deployment is defined.

    Example:
      .. code-block:: yaml

        deployments:
          - modules:  # minimum requirements for a deployment
              - my-module.cfn
            regions:
              - us-east-1
          - name: detailed-deployment  # optional
            modules:
              - path: my-other-modules.cfn
            regions:
              - us-east-1
            account-id:  # optional
              - dev: 0000
              - prod: 1111
            assume-role:  # optional
              dev: arn:aws:iam::0000:role/role-name
              prod: arn:aws:iam::1111:role/role-name
            environments:  # optional
              dev:
                region: us-east-1
                image_id: ami-abc123
            env_vars:  # optional environment variable overrides
              dev:
                AWS_PROFILE: foo
                APP_PATH:  # a list will be treated as components of a path on disk
                  - myapp.tf
                  - foo
              prod:
                AWS_PROFILE: bar
                APP_PATH:
                  - myapp.tf
                  - foo
              "*":  # applied to all environments
                ANOTHER_VAR: foo
              skip-npm-ci: false  # optional

    A deployment can be defined without modules if the directory
    containing the Runway config file is a module directory.

    Example:
      .. code-block:: yaml

        deployments:
          - current_dir: true
            regions:
              - us-west-2
            assume-role:
              arn: arn:aws:iam::0000:role/role-name

    """

    def __init__(self, deployment):
        # type: (Dict[str, Any]) -> None
        """.. Runway deployment definition.

        Keyword Args:
            account-alias (Optional[Dict[str, str]]): A mapping of
                ``$environment: $alias`` that, if provided, is used to
                verify the currently assumed role or credentials.
            account-id (Optional[Dict[str, Union[str, int]]]): A mapping
                of ``$environment: $id`` that, if provided, is used to
                verify the currently assumed role or credentials.
            assume-role (Optional[Dict[str, Union[str, Dict[str, str]]]]):
                A mapping of ``$environment: $role`` or
                ``$environment: {arn: $role, duration: $int}`` to assume
                a role when processing a deployment. ``arn: $role`` can
                be used to apply the same role to all environment.
                ``post_deploy_env_revert: true`` can also be provided to
                revert credentials after processing.
            current_dir (bool): Used to deploy the module in which the
                Runway config file is located. *(default: false)*
            environments (Optional[Dict[str, Dict[str, Any]]]): Mapping for
                variables to environment names. When run, the variables
                defined here are merged with those in the
                ``.env``/``.tfenv``/environment config file and
                environments section of each module.
            env_vars (Optional[Dict[str, Dict[str, Any]]]): A mapping of
                OS environment variable overrides to apply when processing
                modules in the deployment. Can be defined per environment
                or for all environments using ``"*"`` as the environment
                name.
            modules (Optional[List[Dict[str, Any]]]): A list of modules
                to be processed in the order they are defined.
            module_options (Optional[Dict[str, Any]]): Options that are
                shared among all modules in the deployment.
            name (str): Name of the deployment. Used to more easily
                identify where different deployments begin/end in the logs.
            regions (List[str]): AWS region names where modules will be
                deployed/destroyed.
            skip-npm-ci (bool): Omits npm ci execution during Serverless
                deployments. (i.e. for use with pre-packaged
                node_modules) *(default: false)*

        References:
            - :class:`module<runway.config.ModuleDefinition>`
            - :ref:`command-deploy`
            - :ref:`command-destroy`
            - :ref:`command-plan`

        """
        self.account_alias = deployment.pop(
            'account_alias', deployment.pop('account-alias', {})
        )  # type: Optional[Dict[str, str]]
        self.account_id = deployment.pop(
            'account_id', deployment.pop('account-id', {})
        )  # type: Optional[Dict[str, Union[str, int]]]
        self.assume_role = deployment.pop(
            'assume_role', deployment.pop('assume-role', {})
        )  # type: Optional[Dict[str, Union[str, Dict[str, str]]]]
        self.current_dir = deployment.pop('current_dir', False)  # type: bool
        self.environments = deployment.pop(
            'environments', {}
        )  # type: Optional[Dict[str, Dict[str, Any]]]
        self.env_vars = deployment.pop(
            'env_vars', {}
        )  # type: Optional[Dict[str, Dict[str, Any]]]
        self.modules = ModuleDefinition.from_list(
            deployment.pop('modules', [])  # can be none if current_dir
        )  # type: List[ModuleDefinition]
        self.module_options = deployment.pop(
            'module_options', {}
        )  # type: Optional(Dict[str, Any])
        self.name = deployment.pop('name')  # type: str
        self.regions = deployment.pop('regions', [])  # type: List[str]
        self.skip_npm_ci = deployment.pop(
            'skip_npm_ci', deployment.pop('skip-npm-ci', False)
        )  # type: bool

        if deployment:
            LOGGER.warning(
                'Invalid keys found in deployment %s have been ignored: %s',
                self.name, ', '.join(deployment.keys())
            )

    @classmethod
    def from_list(cls, deployments):
        """Instantiate DeploymentDefinitions from a list."""
        results = []
        for i, deployment in enumerate(deployments):
            if not deployment.get('name'):
                deployment['name'] = 'deployment_{}'.format(str(i + 1))
            results.append(cls(deployment))
        return results


class TestDefinition(ConfigComponent):
    """Tests can be defined as part of the Runway config file.

    This is to remove the need for complex Makefiles or scripts to initiate
    test runners. Simply define all tests for a project in the Runway
    config file and use the ``runway test`` :ref:`command<command-test>`
    to execute them.

    Example:
      .. code-block:: yaml

        tests:
          - name: my-test
            type: script
            required: false
            args:
              commands:
                - echo "Hello World!"

    """

    def __init__(self,
                 name,  # type: str
                 test_type,  # type: str
                 args=None,  # type: Optional[Dict[str, Any]]
                 required=True  # type: bool
                 # pylint only complains for python2
                 ):  # pylint: disable=bad-continuation
        # type: (...) -> None
        """.. Runway test definitions.

        Keyword Args:
            name (str): Name of the test. Used to more easily identify
                where different tests begin/end in the logs.
            type (str): The type of test to run. See
                :ref:`Build-in Test Types<built-in-test-types>`
                for supported test types.
            args (Optional[Dict[str, Any]]): Arguments to be passed to
                the test. Supported arguments vary by test type. See
                :ref:`Build-in Test Types<built-in-test-types>` for the
                list of arguments supported by each test type.
            required (bool):  If false, testing will continue if the test
                fails. *(default: true)*

        References:
            - :ref:`Build-in Test Types<built-in-test-types>` - Supported
              test types and their
              arguments
            - :ref:`test command<command-test>`

        """
        self.name = name
        self.type = test_type
        self.args = args or {}
        self.required = required

    @classmethod
    def from_list(cls, tests):
        # type: (List[Dict[str, Any]]) -> List[TestDefinition]
        """Instantiate TestDefinitions from a list."""
        results = []

        for index, test in enumerate(tests):
            name = test.pop('name', 'test_{}'.format(index + 1))
            results.append(cls(name, test.pop('type'),
                               test.pop('args', {}),
                               test.pop('required', False)))

            if test:
                LOGGER.warning(
                    'Invalid keys found in test %s have been ignored: %s',
                    name, ', '.join(test.keys())
                )
        return results


class Config(ConfigComponent):
    """The Runway config file is where all options are defined.

    It contains definitions for deployments, tests, and some global
    options that impact core functionality.

    The Runway config file can have two possible names, ``runway.yml``
    or ``runway.yaml``. It must be stored at the root of the directory
    containing all modules to be deployed.

    Example:
        .. code-block:: yaml

            ---
            # See full syntax at https://github.com/onicagroup/runway
            ignore_git_branch: true
            tests:
              - name: example
                type: script
                args:
                  commands:
                    - echo "Hello world"
            deployments:
              - modules:
                  - path: my-modules.cfn
                regions:
                  - us-east-1

    """

    accepted_names = ['runway.yml', 'runway.yaml']

    def __init__(self,
                 deployments,  # type: List[Dict[str, Any]]
                 tests=None,  # type: List[Dict[str, Any]]
                 ignore_git_branch=False  # type: bool
                 # pylint only complains for python2
                 ):  # pylint: disable=bad-continuation
        # type: (...) -> None
        """.. Top-level Runway config file.

        Keyword Args:
            deployments (List[Dict[str, Any]]): A list of
                :class:`deployments<runway.config.DeploymentDefinition>`
                that are processed in the order they are defined.
            tests (Optional[List[Dict[str, Any]]]): A list of
                :class:`tests<runway.config.TestDefinition>` that are
                processed in the order they are defined.
            ignore_git_branch (bool): Disable git branch lookup when
                using environment folders, Mercurial, or defining the
                ``DEPLOY_ENVIRONMENT`` environment variable before
                execution. Note that defining ``DEPLOY_ENVIRONMENT``
                will automatically ignore the git branch.

        References:
            - :class:`deployment<runway.config.DeploymentDefinition>`
            - :class:`test<runway.config.TestDefinition>`

        """
        self.deployments = DeploymentDefinition.from_list(deployments)
        self.tests = TestDefinition.from_list(tests)
        self.ignore_git_branch = ignore_git_branch

    @classmethod
    def load_from_file(cls, config_path):
        # type: (str) -> Config
        """Load config file into a Config object."""
        if not os.path.isfile(config_path):
            LOGGER.error("Runway config file was not found (looking for "
                         "%s)",
                         config_path)
            sys.exit(1)
        with open(config_path) as data_file:
            config_file = yaml.safe_load(data_file)
            result = Config(config_file.pop('deployments'),
                            config_file.pop('tests', []),
                            config_file.pop('ignore_git_branch', False))

            if config_file:
                LOGGER.warning(
                    'Invalid keys found in runway file have been ignored: %s',
                    ', '.join(config_file.keys())
                )
            return result

    @classmethod
    def find_config_file(cls, config_dir=None):
        # type: (Optional[str]) -> str
        """Find the Runway config file."""
        if not config_dir:
            config_dir = os.getcwd()

        for name in cls.accepted_names:
            conf_path = os.path.join(config_dir, name)
            if os.path.isfile(conf_path):
                return conf_path

        LOGGER.error('Runway config file was not found. Looking for one '
                     'of %s in %s', str(cls.accepted_names), config_dir)
        sys.exit(1)
