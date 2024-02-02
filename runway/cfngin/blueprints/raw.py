"""CFNgin blueprint representing raw template module."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from jinja2 import Environment, FileSystemLoader

from ...compat import cached_property
from ..exceptions import InvalidConfig, UnresolvedBlueprintVariable
from ..utils import parse_cloudformation_template
from .base import Blueprint

if TYPE_CHECKING:
    from ...context import CfnginContext
    from ...variables import Variable

LOGGER = logging.getLogger(__name__)


def get_template_path(file_path: Path) -> Optional[Path]:
    """Find raw template in working directory or in sys.path.

    template_path from config may refer to templates co-located with the CFNgin
    config, or files in remote package_sources. Here, we emulate python module
    loading to find the path to the template.

    Args:
        filename: Template path.

    Returns:
        Path to file, or None if no file found

    """
    if file_path.is_file():
        return file_path
    for i in sys.path:
        test_path = Path(i) / file_path.name
        if test_path.is_file():
            return test_path
    return None


def resolve_variable(provided_variable: Optional[Variable], blueprint_name: str) -> Any:
    """Resolve a provided variable value against the variable definition.

    This acts as a subset of resolve_variable logic in the base module, leaving
    out everything that doesn't apply to CFN parameters.

    Args:
        provided_variable: The variable value provided to the blueprint.
        blueprint_name: The name of the blueprint that the variable is
            being applied to.

    Raises:
        UnresolvedBlueprintVariable: Raised when the provided variable is
            not already resolved.

    """
    value = None
    if provided_variable:
        if not provided_variable.resolved:
            raise UnresolvedBlueprintVariable(blueprint_name, provided_variable)

        value = provided_variable.value

    return value


class RawTemplateBlueprint(Blueprint):  # pylint: disable=abstract-method
    """Blueprint class for blueprints auto-generated from raw templates.

    Attributes:
        context: CFNgin context object.
        description: The description of the CloudFormation template that will
            be generated by this Blueprint.
        mappings: CloudFormation Mappings to be added to the template during the
            rendering process.
        name: Name of the Stack that will be created by the Blueprint.
        raw_template_path: Path to the raw CloudFormation template file.

    """

    raw_template_path: Path

    def __init__(  # pylint: disable=super-init-not-called
        self,
        name: str,
        context: CfnginContext,
        *,
        description: Optional[str] = None,
        mappings: Optional[Dict[str, Any]] = None,
        raw_template_path: Path,
        **_: Any,
    ) -> None:
        """Instantiate class.

        .. versionchanged:: 2.0.0
            Class only takes 2 positional arguments.
            The rest are now keyword arguments.

        """
        self._rendered = None
        self._resolved_variables = None
        self._version = None
        self.context = context
        self.description = description
        self.mappings = mappings
        self.name = name
        self.raw_template_path = raw_template_path

    @property
    def output_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Get the output definitions.

        .. versionadded:: 2.0.0

        Returns:
            Output definitions. Keys are output names, the values are dicts
            containing key/values for various output properties.

        """
        return self.to_dict().get("Outputs", {})

    @cached_property
    def parameter_definitions(self) -> Dict[str, Any]:
        """Get the parameter definitions to submit to CloudFormation.

        .. versionadded:: 2.0.0

        Returns:
            Parameter definitions. Keys are parameter names, the values are dicts
            containing key/values for various parameter properties.

        """
        return self.to_dict().get("Parameters", {})

    @cached_property
    def parameter_values(self) -> Dict[str, Union[List[Any], str]]:
        """Return a dict of variables with type :class:`~runway.cfngin.blueprints.variables.types.CFNType`.

        .. versionadded:: 2.0.0

        Returns:
            Variables that need to be submitted as CloudFormation Parameters.
            Will be a dictionary of ``<parameter name>: <parameter value>``.

        """  # noqa
        return self._resolved_variables or {}

    @property
    def rendered(self) -> str:
        """Return (generating first if needed) rendered template."""
        if not self._rendered:
            template_path = get_template_path(self.raw_template_path)
            if template_path:
                if len(os.path.splitext(template_path)) == 2 and (
                    os.path.splitext(template_path)[1] == ".j2"
                ):
                    self._rendered = (
                        Environment(
                            loader=FileSystemLoader(
                                searchpath=os.path.dirname(template_path)
                            )
                        )
                        .get_template(os.path.basename(template_path))
                        .render(
                            context=self.context,
                            mappings=self.mappings,
                            name=self.name,
                            variables=self._resolved_variables,
                        )
                    )
                else:
                    with open(template_path, "r", encoding="utf-8") as template:
                        self._rendered = template.read()
            else:
                raise InvalidConfig(f"Could not find template {self.raw_template_path}")
            # clear cached properties that rely on this property
            self._del_cached_property("parameter_definitions")

        return self._rendered

    @property
    def requires_change_set(self) -> bool:
        """Return True if the underlying template has transforms."""
        return bool("Transform" in self.to_dict())

    @property
    def version(self) -> str:
        """Return (generating first if needed) version hash."""
        if not self._version:
            self._version = hashlib.md5(self.rendered.encode()).hexdigest()[:8]
        return self._version

    def to_dict(self) -> Dict[str, Any]:
        """Return the template as a python dictionary.

        Returns:
            dict: the loaded template as a python dictionary

        """
        return parse_cloudformation_template(self.rendered)

    def to_json(self, variables: Optional[Dict[str, Any]] = None) -> str:
        """Return the template in JSON.

        Args:
            variables: Unused in this subclass (variables won't affect the template).

        """
        # load -> dumps will produce json from json or yaml templates
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    def render_template(self) -> Tuple[str, str]:
        """Load template and generate its md5 hash."""
        return (self.version, self.rendered)

    def resolve_variables(self, provided_variables: List[Variable]) -> None:
        """Resolve the values of the blueprint variables.

        This will resolve the values of the template parameters with values
        from the env file, the config, and any lookups resolved. The
        resolution is run twice, in case the blueprint is jinja2 templated
        and requires provided variables to render.

        Args:
            provided_variables: List of provided variables.

        """
        # Pass 1 to set resolved_variables to provided variables
        self._resolved_variables = {}
        variable_dict = {var.name: var for var in provided_variables}
        for var_name, _var_def in variable_dict.items():
            value = resolve_variable(variable_dict.get(var_name), self.name)
            if value is not None:
                self._resolved_variables[var_name] = value

        # Pass 2 to render the blueprint and set resolved_variables according
        # to defined variables
        # save a copy of param defs before clearing resolved var dict
        defined_variables = self.parameter_definitions.copy()
        self._resolved_variables = {}
        variable_dict = {var.name: var for var in provided_variables}
        for var_name, _var_def in defined_variables.items():
            value = resolve_variable(variable_dict.get(var_name), self.name)
            if value is not None:
                self._resolved_variables[var_name] = value
        # clear cached properties that rely on the property set by this
        self._del_cached_property("parameter_values")
