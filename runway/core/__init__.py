"""Core Runway API."""
import logging as _logging
import sys as _sys
import traceback as _traceback
from typing import (TYPE_CHECKING, Any, Dict, List,  # noqa pylint: disable=W
                    Optional)

from ..context import Context
from ..tests.registry import TEST_HANDLERS as _TEST_HANDLERS
from . import components, providers

if TYPE_CHECKING:
    from ..config import Config, DeploymentDefinition

LOGGER = _logging.getLogger(__name__)

__all__ = [
    'Runway',
    'components',
    'providers'
]


class Runway(object):
    """Runway's core functionality."""

    def __init__(self, config, context=None):
        # type: (Config, Optional[Context]) -> None
        """Instantiate class.

        Args:
            config: Runway config.
            context: Runway context.

        """
        self.deployments = config.deployments
        self.future = config.future
        self.tests = config.tests
        self.ignore_git_branch = config.ignore_git_branch
        self.variables = config.variables

        if context:
            self.ctx = context
        else:
            self.ctx = Context(
                deploy_environment=components.DeployEnvironment(
                    ignore_git_branch=self.ignore_git_branch
                )
            )
        self.ctx.env.log_name()

    def deploy(self, deployments=None):
        # type: (Optional[List[DeploymentDefinition]]) -> None
        """Deploy action.

        Args:
            deployments: List of deployments to run. If not provided,
                all deployments in the config will be run.

        """
        self.__run_action('deploy', deployments if deployments is not None else
                          self.deployments)

    def destroy(self, deployments=None):
        # type: (Optional[List[DeploymentDefinition]]) -> None
        """Destroy action.

        Args:
            deployments: List of deployments to run. If not provided,
                all deployments in the config will be run in reverse.

        """
        self.__run_action('destroy', deployments if deployments is not None else
                          self.reverse_deployments(self.deployments))
        if not deployments:
            # return config attribute to original state
            self.reverse_deployments(self.deployments)

    def get_env_vars(self, deployments=None):
        # type: (Optional[List[DeploymentDefinition]]) -> Dict[str, Any]
        """Get env_vars defined in the config.

        Args:
            deployments: List of deployments to get env_vars from.

        Returns:
            Resolved env_vars from the deployments.

        """
        deployments = deployments or self.deployments
        result = {}
        for deployment in deployments:
            obj = components.Deployment(context=self.ctx,
                                        definition=deployment,
                                        variables=self.variables)
            result.update(obj.env_vars_config)
        return result

    def plan(self, deployments=None):
        # type: (Optional[List[DeploymentDefinition]]) -> None
        """Plan action.

        Args:
            deployments: List of deployments to run. If not provided,
                all deployments in the config will be run.

        """
        self.__run_action('plan', deployments if deployments is not None else
                          self.deployments)

    @staticmethod
    def reverse_deployments(deployments):
        # type: (List[DeploymentDefinition]) -> List[DeploymentDefinition]
        """Reverse deployments and the modules within them.

        Args:
            deployments: List of deployments to reverse.

        Returns:
            Deployments and modules in reverse order.

        """
        result = []
        for deployment in deployments:
            deployment.reverse()
            result.insert(0, deployment)
        return result

    def test(self):
        """Run tests defined in the config."""
        if not self.tests:
            LOGGER.error(
                'Use of "runway test" without defining tests in the runway config '
                'file has been removed. See '
                'https://docs.onica.com/projects/runway/en/release/defining_tests.html'
            )
            LOGGER.error('E.g.:')
            for i in ['tests:',
                      '  - name: example-test',
                      '    type: script',
                      '    required: true',
                      '    args:',
                      '      commands:',
                      '        - echo "Success!"',
                      '']:
                print(i)
            _sys.exit(1)
        self.ctx.command = 'test'

        failed_tests = []

        LOGGER.info('Found %i test(s)', len(self.tests))
        for tst in self.tests:
            tst.resolve(self.ctx, variables=self.variables)
            LOGGER.info("")
            LOGGER.info("")
            LOGGER.info("======= Running test '%s' ===========================",
                        tst.name)
            try:
                handler = _TEST_HANDLERS[tst.type]
            except KeyError:
                LOGGER.error('Unable to find handler for test "%s" of '
                             'type "%s"', tst.name, tst.type)
                if tst.required:
                    _sys.exit(1)
                failed_tests.append(tst.name)
                continue
            try:
                handler.handle(tst.name, tst.args)
            except (Exception, SystemExit) as err:  # pylint: disable=broad-except
                # for lack of an easy, better way to do this atm, assume
                # SystemExits are due to a test failure and the failure reason
                # has already been properly logged by the handler or the
                # tool it is wrapping.
                if not isinstance(err, SystemExit):
                    _traceback.print_exc()
                elif err.code == 0:
                    continue  # tests with zero exit code don't indicate failure
                LOGGER.error('Test failed: %s', tst.name)
                if tst.required:
                    LOGGER.error('Failed test was required, the remaining '
                                 'tests have been skipped')
                    _sys.exit(1)
                failed_tests.append(tst.name)
        if failed_tests:
            LOGGER.error('The following tests failed: %s',
                         ', '.join(failed_tests))
            _sys.exit(1)

    def __run_action(self, action, deployments):
        # type: (Optional[List[DeploymentDefinition]]) -> None
        """Run an action on a list of deployments.

        Args:
            action: Name of the action.
            deployments: List of deployments to run.

        """
        self.ctx.command = action
        components.Deployment.run_list(action=action,
                                       context=self.ctx,
                                       deployments=deployments,
                                       future=self.future,
                                       variables=self.variables)
