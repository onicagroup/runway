"""Blueprint for an admin user."""
# pylint: disable=no-self-use
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Final, Optional

from troposphere import NoValue
from troposphere.iam import User

from runway.cfngin.blueprints.base import Blueprint
from runway.compat import cached_property

if TYPE_CHECKING:
    from runway.cfngin.blueprints.type_defs import BlueprintVariableTypeDef


class AdminUser(Blueprint):
    """Blueprint for an admin user."""

    VARIABLES: Final[Dict[str, BlueprintVariableTypeDef]] = {
        "PermissionsBoundary": {"type": str},
        "UserName": {"type": str, "default": ""},
    }

    @cached_property
    def namespace(self) -> str:
        """Stack namespace."""
        return self.context.namespace

    @cached_property
    def username(self) -> Optional[str]:
        """Name of the user being created."""
        val = self.variables["UserName"]
        if val == "":
            return None
        return val

    def create_template(self) -> None:
        """Create a template from the Blueprint."""
        self.template.set_description("Admin user")
        self.template.set_version("2010-09-09")

        user = User(  # TODO refine permissions
            "User",
            template=self.template,
            ManagedPolicyArns=["arn:aws:iam::aws:policy/AdministratorAccess"],
            PermissionsBoundary=self.variables["PermissionsBoundary"],
            UserName=self.username or NoValue,
        )
        self.add_output(user.title, user.ref())
        self.add_output(f"{user.title}Arn", user.get_att("Arn"))
