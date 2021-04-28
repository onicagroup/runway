"""K8s (kustomize) module."""
from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, cast

from .._logging import PrefixAdaptor
from ..compat import cached_property
from ..config.models.runway.options.k8s import RunwayK8sModuleOptionsDataModel
from ..core.components import DeployEnvironment
from ..env_mgr.kbenv import KB_VERSION_FILENAME, KBEnvManager
from ..util import DOC_SITE, which
from .base import ModuleOptions, RunwayModule
from .utils import run_module_command

if TYPE_CHECKING:
    from .._logging import RunwayLogger
    from ..context import RunwayContext

LOGGER = cast("RunwayLogger", logging.getLogger(__name__))


class K8s(RunwayModule):
    """Kubectl Runway Module."""

    options: K8sOptions

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
            options=K8sOptions.parse_obj(
                deploy_environment=context.env, obj=options or {}, path=module_root
            ),
            parameters=parameters,
        )
        # logger needs to be created here to use the correct logger
        self.logger = PrefixAdaptor(self.name, LOGGER)

    @property
    def skip(self) -> bool:
        """Determine if the module should be skipped."""
        if self.options.kustomize_config.is_file():
            LOGGER.info(
                "processing kustomize overlay: %s", self.options.kustomize_config
            )
            return False
        LOGGER.info(
            "skipped; kustomize overlay for this environment/region not"
            " found -- looking for one of: %s",
            ", ".join(
                str(self.path / "overlays" / i / "kustomization.yaml")
                for i in self.options.gen_overlay_dirs(
                    self.ctx.env.name, self.ctx.env.aws_region
                )
            ),
        )
        return True

    def run_kubectl(self, command: str = "plan") -> Dict[str, bool]:
        """Run kubectl."""
        if self.skip:
            return {"skipped_configs": True}

        if self.options.kubectl_version:
            self.logger.debug("using kubectl version from the module definition")
            k8s_bin = KBEnvManager(self.path).install(self.options.kubectl_version)
        elif (self.options.kustomize_config / KB_VERSION_FILENAME).is_file():
            self.logger.debug(
                "using kubectl version from the overlay directory: %s",
                self.options.kustomize_config,
            )
            k8s_bin = KBEnvManager(self.options.kustomize_config).install()
        elif (self.path / KB_VERSION_FILENAME).is_file():
            self.logger.debug(
                "using kubectl version from the module directory: %s", self.path
            )
            k8s_bin = KBEnvManager(self.path).install()
        elif (self.ctx.env.root_dir / KB_VERSION_FILENAME).is_file():
            file_path = self.ctx.env.root_dir / KB_VERSION_FILENAME
            self.logger.debug(
                "using kubectl version from the project's root directory: %s",
                file_path,
            )
            k8s_bin = KBEnvManager(self.ctx.env.root_dir).install()
        else:
            self.logger.debug("kubectl version not specified; checking path")
            if not which("kubectl"):
                self.logger.error(
                    "kubectl not available and a version to install not specified"
                )
                self.logger.error(
                    "learn how to use Runway to manage kubectl versions at %s"
                    "/page/kubernetes/advanced_features.html#version-management",
                    DOC_SITE,
                )
                sys.exit(1)
            k8s_bin = "kubectl"

        kustomize_cmd = [k8s_bin, "kustomize", str(self.options.kustomize_config)]
        self.logger.debug("running kubectl command: %s", " ".join(kustomize_cmd))
        kustomize_yml = subprocess.check_output(
            kustomize_cmd, env=self.ctx.env.vars
        ).decode()
        if command == "plan":
            self.logger.info("yaml was generated by kubectl:\n\n%s", kustomize_yml)
        else:
            self.logger.debug("yaml generated by kubectl:\n\n%s", kustomize_yml)
        if command in ["apply", "delete"]:
            kubectl_command = [k8s_bin, command]
            if command == "delete":
                kubectl_command.append("--ignore-not-found=true")
            kubectl_command.extend(["-k", str(self.options.kustomize_config)])

            self.logger.info("%s (in progress)", command)
            self.logger.debug("running kubectl command: %s", " ".join(kubectl_command))
            run_module_command(kubectl_command, self.ctx.env.vars, logger=self.logger)
            self.logger.info("%s (complete)", command)
        return {"skipped_configs": False}

    def plan(self) -> None:
        """Run kustomize build and display generated plan."""
        self.run_kubectl(command="plan")

    def deploy(self) -> None:
        """Run kubectl apply."""
        self.run_kubectl(command="apply")

    def destroy(self) -> None:
        """Run kubectl delete."""
        self.run_kubectl(command="delete")


class K8sOptions(ModuleOptions):
    """Module options for Kubernetes.

    Attributes:
        data: Options parsed into a data model.
        kubectl_version: Version of kubectl to use.
        overlay_path: Explicit directory containing the kustomize overlay to use.

    """

    def __init__(
        self,
        data: RunwayK8sModuleOptionsDataModel,
        deploy_environment: DeployEnvironment,
        path: Path,
    ) -> None:
        """Instantiate class.

        Args:
            data: Options parsed into a data model.
            deploy_environment: Current deploy environment.
            path: Module path.

        """
        self.data = data
        self.env = deploy_environment
        self.kubectl_version = data.kubectl_version
        self.path = path

    @cached_property
    def kustomize_config(self) -> Path:
        """Kustomize configuration file."""
        return self.overlay_path / "kustomization.yaml"

    @cached_property
    def overlay_path(self) -> Path:
        """Directory containing the kustomize overlay to use."""
        if self.data.overlay_path:
            return self.data.overlay_path
        return self.get_overlay_dir(
            path=self.path / "overlays",
            environment=self.env.name,
            region=self.env.aws_region,
        )

    @staticmethod
    def gen_overlay_dirs(environment: str, region: str) -> List[str]:
        """Generate possible overlay directories.

        Prefers more explicit direcory name but falls back to environmet name only.

        Args:
            environment: Current deploy environment.
            region : Current AWS region.

        """
        return [f"{environment}-{region}", environment]

    @classmethod
    def get_overlay_dir(cls, path: Path, environment: str, region: str) -> Path:
        """Determine the overlay directory to use."""
        overlay_dir = path
        for name in cls.gen_overlay_dirs(environment, region):
            overlay_dir = path / name
            if (overlay_dir / "kustomization.yaml").is_file():
                return overlay_dir
        return overlay_dir

    @classmethod
    def parse_obj(
        cls,
        deploy_environment: DeployEnvironment,
        obj: object,
        path: Optional[Path] = None,
    ) -> K8sOptions:
        """Parse options definition and return an options object.

        Args:
            deploy_environment: Current deploy environment.
            obj: Object to parse.
            path: Module path.

        """
        return cls(
            data=RunwayK8sModuleOptionsDataModel.parse_obj(obj),
            deploy_environment=deploy_environment,
            path=path or Path.cwd(),
        )
