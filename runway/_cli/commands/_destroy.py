"""``runway destroy`` command."""

# docs: file://./../../../docs/source/commands.rst
import logging
from typing import Any

import click
from pydantic import ValidationError

from ...core import Runway
from ...exceptions import ConfigNotFound, VariablesFileNotFound
from .. import options
from ..utils import select_deployments

LOGGER = logging.getLogger(__name__.replace("._", "."))


@click.command("destroy", short_help="destroy things")
@options.ci
@options.debug
@options.deploy_environment
@options.no_color
@options.tags
@options.verbose
@click.pass_context
def destroy(ctx: click.Context, debug: bool, tags: tuple[str, ...], **_: Any) -> None:
    """Destroy infrastructure as code.

    \b
    Process
    -------
    1. Determines the deploy environment.
        - "-e, --deploy-environment" option
        - "DEPLOY_ENVIRONMENT" environment variable
        - git branch name
            - strips "ENV-" prefix, master is converted to common
            - ignored if "ignore_git_branch: true"
        - name of the current working directory
    2. Selects deployments & modules to deploy.
        - (default) prompts
        - (tags) module contains all tags
        - (non-interactive) all
    3. Destroys selected deployments/modules in reverse the order defined.

    """  # noqa: D301
    if not ctx.obj.env.ci:
        click.secho(
            "[WARNING] Runway is about to be run in DESTROY mode. [WARNING]",
            bold=True,
            fg="red",
        )
        click.secho(
            "Any/all deployment(s) selected will be irrecoverably DESTROYED.",
            bold=True,
            fg="red",
        )
        if not click.confirm("\nProceed?"):
            ctx.exit(0)
        click.echo("")
    try:
        Runway(ctx.obj.runway_config, ctx.obj.get_runway_context()).destroy(
            Runway.reverse_deployments(
                select_deployments(ctx, ctx.obj.runway_config.deployments, tags)
            )
        )
    except ValidationError as err:
        LOGGER.error(err, exc_info=debug)
        ctx.exit(1)
    except (ConfigNotFound, VariablesFileNotFound) as err:
        LOGGER.error(err.message, exc_info=debug)
        ctx.exit(1)
