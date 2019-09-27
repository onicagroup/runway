"""Execute the embedded copy of `Stacker`_.

Runway's embedded version of `Stacker`_ is generally updated with new
features much quicker than mainstream `Stacker`_. There are times when
a `Stacker`_ deployment will be successful with runway and not with
mainstream `Stacker`_ because of this so, runway exposes it's embedded
`Stacker`_ for standalone use.

Example:
  .. code-block:: shell

    $ runway run-stacker build example.env example.yaml

"""

import logging
# import platform
import sys

from ..runway_command import RunwayCommand
from ...util import get_embedded_lib_path

LOGGER = logging.getLogger('runway')


def strip_leading_option_delim(args):
    """Remove leading -- if present.

    Using the "--" end of options syntax bypasses docopt's parsing of options.
    """
    if len(args) > 1:
        if args[0] == '--':
            return args[1:]
    return args


class RunStacker(RunwayCommand):
    """Extend RunwayCommand with execution of Stacker."""

    SKIP_FIND_CONFIG = True

    def execute(self):
        """Execute stacker."""
        cmd_line_args = strip_leading_option_delim(
            self._cli_arguments.get('<stacker-args>', [])
        )
        lib_path = get_embedded_lib_path()
        # this shouldn't be an issue anymore
        # if platform.system().lower() == 'windows':
        #     # Because this will be run via subprocess, the backslashes on Windows
        #     # will cause command errors
        #     lib_path = lib_path.replace('\\', '/')
        sys.argv = ['stacker'] + cmd_line_args
        sys.path.insert(1, lib_path)
        from stacker.logger import setup_logging
        from stacker.commands import Stacker
        stacker = Stacker(setup_logging=setup_logging)
        args = stacker.parse_args(cmd_line_args)
        stacker.configure(args)
        args.run(args)
