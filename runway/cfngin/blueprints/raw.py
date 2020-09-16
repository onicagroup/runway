"""CFNgin blueprint representing raw template module."""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader

from ..exceptions import InvalidConfig, UnresolvedBlueprintVariable
from ..util import parse_cloudformation_template
from .base import Blueprint

if TYPE_CHECKING:
    from ..context import Context


def get_template_path(file_path: Path) -> Optional[Path]:
    """Find raw template in working directory or in sys.path.

    template_path from config may refer to templates colocated with the Stacker
    config, or files in remote package_sources. Here, we emulate python module
    loading to find the path to the template.

    Args:
        filename (Path): Template path.

    Returns:
        Optional[Path]: Path to file, or None if no file found

    """
    if file_path.is_file():
        return file_path
    for i in sys.path:
        test_path = Path(i) / file_path.name
        if test_path.is_file():
            return test_path
    return None


def get_template_params(template):
    """Parse a CFN template for defined parameters.

    Args:
        template (dict): Parsed CFN template.

    Returns:
        dict: Template parameters.

    """
    params = {}

    if "Parameters" in template:
        params = template["Parameters"]
    return params


def resolve_variable(provided_variable, blueprint_name):
    """Resolve a provided variable value against the variable definition.

    This acts as a subset of resolve_variable logic in the base module, leaving
    out everything that doesn't apply to CFN parameters.

    Args:
        provided_variable (:class:`runway.cfngin.variables.Variable`):
            The variable value provided to the blueprint.
        blueprint_name (str): The name of the blueprint that the variable is
            being applied to.

    Returns:
        object: The resolved variable string value.

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
    """Blueprint class for blueprints auto-generated from raw templates."""

    def __init__(  # pylint: disable=super-init-not-called
        self,
        name: str,
        context: Context,
        raw_template_path: Path,
        mappings: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
    ) -> None:
        """Instantiate class."""
        self.name = name
        self.context = context
        self.mappings = mappings
        self.resolved_variables = None
        self.raw_template_path = raw_template_path
        self._rendered = None
        self._version = None

    def to_json(self, variables=None):
        """Return the template in JSON.

        Args:
            variables (dict):
                Unused in this subclass (variables won't affect the template).

        Returns:
            str: the rendered CFN JSON template

        """
        # load -> dumps will produce json from json or yaml templates
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    def to_dict(self):
        """Return the template as a python dictionary.

        Returns:
            dict: the loaded template as a python dictionary

        """
        return parse_cloudformation_template(self.rendered)

    def render_template(self):
        """Load template and generate its md5 hash."""
        return (self.version, self.rendered)

    def get_parameter_definitions(self):
        """Get the parameter definitions to submit to CloudFormation.

        Returns:
            Dict[str, Any]: parameter definitions. Keys are parameter names,
            the values are dicts containing key/values for various parameter
            properties.

        """
        return get_template_params(self.to_dict())

    def get_output_definitions(self):
        """Get the output definitions.

        Returns:
            Dict[str, Any]: output definitions. Keys are output names, the
            values are dicts containing key/values for various output
            properties.

        """
        return self.to_dict().get("Outputs", {})

    def resolve_variables(self, provided_variables):
        """Resolve the values of the blueprint variables.

        This will resolve the values of the template parameters with values
        from the env file, the config, and any lookups resolved. The
        resolution is run twice, in case the blueprint is jinja2 templated
        and requires provided variables to render.

        Args:
            provided_variables (List[:class:`runway.cfngin.variables.Variable`]):
                List of provided variables.

        """
        # Pass 1 to set resolved_variables to provided variables
        self.resolved_variables = {}
        variable_dict = dict((var.name, var) for var in provided_variables)
        for var_name, _var_def in variable_dict.items():
            value = resolve_variable(variable_dict.get(var_name), self.name)
            if value is not None:
                self.resolved_variables[var_name] = value

        # Pass 2 to render the blueprint and set resolved_variables according
        # to defined variables
        defined_variables = self.get_parameter_definitions()
        self.resolved_variables = {}
        variable_dict = dict((var.name, var) for var in provided_variables)
        for var_name, _var_def in defined_variables.items():
            value = resolve_variable(variable_dict.get(var_name), self.name)
            if value is not None:
                self.resolved_variables[var_name] = value

    def get_parameter_values(self):
        """Return a dictionary of variables with `type` :class:`CFNType`.

        Returns:
            Dict[str, Any]: variables that need to be submitted as
            CloudFormation Parameters. Will be a dictionary of
            ``<parameter name>: <parameter value>``.

        """
        return self.resolved_variables

    @property
    def requires_change_set(self):
        """Return True if the underlying template has transforms."""
        return bool("Transform" in self.to_dict())

    @property
    def rendered(self):
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
                            variables=self.resolved_variables,
                        )
                    )
                else:
                    with open(template_path, "r") as template:
                        self._rendered = template.read()
            else:
                raise InvalidConfig(
                    "Could not find template %s" % self.raw_template_path
                )

        return self._rendered

    @property
    def version(self):
        """Return (generating first if needed) version hash."""
        if not self._version:
            self._version = hashlib.md5(self.rendered.encode()).hexdigest()[:8]
        return self._version
