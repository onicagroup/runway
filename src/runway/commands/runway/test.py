"""The test command."""
import logging
import sys
import traceback

from ..base_command import BaseCommand
from ...tests.regestry import TEST_HANDLERS

LOGGER = logging.getLogger('runway')


class Test(BaseCommand):  # pylint: disable=too-few-public-methods
    """Execute the test blocks of a runway config."""

    def execute(self):
        """Execute the test blocks of a runway config."""
        test_definitions = self.runway_config.tests

        if not test_definitions:
            LOGGER.warning('Use of "runway test" without defining '
                           'tests in the runway config file has been '
                           'deprecated.')
            sys.exit(1)

        LOGGER.info('Found %i test(s)', len(test_definitions))
        for test in test_definitions:
            LOGGER.info("")
            LOGGER.info("")
            LOGGER.info("======= Running test '%s' ===========================",
                        test.name)
            try:
                handler = TEST_HANDLERS[test.type]
            except KeyError:
                LOGGER.error('Unable to find handler for test %s of '
                             'type %s', test.name, test.type)
                if test.required:
                    sys.exit(1)
                continue
            try:
                handler.handle(test.name, test.args)
            except (Exception, SystemExit) as err:  # pylint: disable=broad-except
                # for lack of an easy, better way to do this atm, assume
                # SystemExits are due to a test failure and the failure reason
                # has already been properly logged by the handler or the
                # tool it is wrapping.
                if not isinstance(err, SystemExit):
                    traceback.print_exc()
                LOGGER.error('Test failed: %s', test.name)
                if test.required:
                    sys.exit(1)
