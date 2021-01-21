"""CDK module."""
from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, cast

from .._logging import PrefixAdaptor
from ..util import change_dir, run_commands, which
from . import generate_node_command, run_module_command
from .base import RunwayModuleNpm

if TYPE_CHECKING:
    from .._logging import RunwayLogger
    from ..context.runway import RunwayContext
    from . import ModuleOptions

LOGGER = cast("RunwayLogger", logging.getLogger(__name__))


def get_cdk_stacks(
    module_path: Path, env_vars: Dict[str, str], context_opts: List[str]
) -> List[str]:
    """Return list of CDK stacks."""
    LOGGER.debug("listing stacks in the CDK app prior to diff...")
    result = subprocess.check_output(
        generate_node_command(
            command="cdk", command_opts=["list"] + context_opts, path=module_path
        ),
        env=env_vars,
    )
    if isinstance(result, bytes):  # python3 returns encoded bytes
        result = result.decode()
    result = result.strip().split("\n")
    LOGGER.debug("found stacks: %s", result)
    return result


class CloudDevelopmentKit(RunwayModuleNpm):
    """CDK Runway Module."""

    def __init__(
        self,
        context: RunwayContext,
        *,
        explicitly_enabled: Optional[bool] = False,
        logger: RunwayLogger = LOGGER,
        module_root: Path,
        name: Optional[str] = None,
        options: Optional[Union[Dict[str, Any], ModuleOptions]] = None,
        parameters: Optional[Dict[str, Any]] = None,
        **_: Any,
    ) -> None:
        """Instantiate class.

        Args:
            context: Runway context object for the current session.
            explicitly_enabled: Whether or not the module is explicitly enabled.
                This is can be set in the event that the current environment being
                deployed to matches the defined environments of the module/deployment.
            logger: Used to write logs.
            module_root: Root path of the module.
            name: Name of the module.
            options: Options passed to the module class from the config as ``options``
                or ``module_options`` if coming from the deployment level.
            parameters: Values to pass to the underlying infrastructure as code
                tool that will alter the resulting infrastructure being deployed.
                Used to templatize IaC.

        """
        super().__init__(
            context,
            explicitly_enabled=explicitly_enabled,
            logger=logger,
            module_root=module_root,
            name=name,
            options=options,
            parameters=parameters,
        )
        # logger needs to be created here to use the correct logger
        self.logger = PrefixAdaptor(self.name, LOGGER)

    def run_cdk(  # pylint: disable=too-many-branches
        self, command: str = "deploy"
    ) -> Dict[str, bool]:
        """Run CDK."""
        response = {"skipped_configs": False}
        cdk_opts = [command]
        if self.context.no_color:
            cdk_opts.append("--no-color")

        if not which("npm"):
            self.logger.error(
                '"npm" not found in path or is not executable; '
                "please ensure it is installed correctly."
            )
            sys.exit(1)

        if "DEBUG" in self.context.env.vars:
            cdk_opts.append("-v")  # Increase logging if requested

        if self.explicitly_enabled:
            if not self.package_json_missing():
                with change_dir(self.path):
                    self.npm_install()
                    if cast(Dict[str, Any], self.options.get("build_steps", [])):
                        self.logger.info("build steps (in progress)")
                        run_commands(
                            commands=cast(
                                List[
                                    Union[
                                        str, List[str], Dict[str, Union[str, List[str]]]
                                    ]
                                ],
                                self.options.get("build_steps", []),
                            ),
                            directory=self.path,
                            env=self.context.env.vars,
                        )
                        self.logger.info("build steps (complete)")
                    cdk_context_opts = []
                    for key, val in cast(Dict[str, str], self.parameters).items():
                        cdk_context_opts.extend(["-c", "%s=%s" % (key, val)])
                    cdk_opts.extend(cdk_context_opts)
                    if command == "diff":
                        self.logger.info("plan (in progress)")
                        for i in get_cdk_stacks(
                            self.path, self.context.env.vars, cdk_context_opts
                        ):
                            subprocess.call(
                                generate_node_command(
                                    "cdk", cdk_opts + [i], self.path  # 'diff <stack>'
                                ),
                                env=self.context.env.vars,
                            )
                        self.logger.info("plan (complete)")
                    else:
                        # Make sure we're targeting all stacks
                        if command in ["deploy", "destroy"]:
                            cdk_opts.append('"*"')

                        if command == "deploy":
                            if "CI" in self.context.env.vars:
                                cdk_opts.append("--ci")
                                cdk_opts.append("--require-approval=never")
                            bootstrap_command = generate_node_command(
                                "cdk",
                                ["bootstrap"]
                                + cdk_context_opts
                                + (["--no-color"] if self.context.no_color else []),
                                self.path,
                            )
                            self.logger.info("bootstrap (in progress)")
                            run_module_command(
                                cmd_list=bootstrap_command,
                                env_vars=self.context.env.vars,
                                logger=self.logger,
                            )
                            self.logger.info("bootstrap (complete)")
                        elif command == "destroy" and self.context.is_noninteractive:
                            cdk_opts.append("-f")  # Don't prompt
                        cdk_command = generate_node_command("cdk", cdk_opts, self.path)
                        self.logger.info("%s (in progress)", command)
                        run_module_command(
                            cmd_list=cdk_command,
                            env_vars=self.context.env.vars,
                            logger=self.logger,
                        )
                        self.logger.info("%s (complete)", command)
            else:
                self.logger.info(
                    'skipped; package.json with "aws-cdk" in devDependencies is '
                    "required for this module type"
                )
        else:
            self.logger.info("skipped; environment required but not defined")
            response["skipped_configs"] = True
        return response

    def plan(self) -> None:
        """Run cdk diff."""
        self.run_cdk(command="diff")

    def deploy(self) -> None:
        """Run cdk deploy."""
        self.run_cdk(command="deploy")

    def destroy(self) -> None:
        """Run cdk destroy."""
        self.run_cdk(command="destroy")
