"""Generate a sample Serverless project using python."""
import logging
import sys

import click

from .utils import TEMPLATES, convert_gitignore, copy_sample

if sys.version_info.major > 2:
    from pathlib import Path  # pylint: disable=E
else:
    from pathlib2 import Path  # pylint: disable=E

LOGGER = logging.getLogger(__name__)


@click.command('sls-py', short_help='sls + python (sampleapp.sls)')
@click.pass_context
def sls_py(ctx):
    # type: (click.Context) -> None
    """Generate a sample Serverless project using python."""
    src = TEMPLATES / 'sls-py'
    dest = Path.cwd() / 'sampleapp.sls'

    copy_sample(ctx, src, dest)
    convert_gitignore(dest / '_gitignore')

    LOGGER.info("Sample Serverless module created at %s", dest)
    LOGGER.info('To finish its setup, change to the %s directory and execute '
                '"npm install" to generate its lockfile.', dest)
