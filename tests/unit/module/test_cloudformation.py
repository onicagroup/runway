"""Test runway.module.cloudformation."""
# pylint: disable=no-self-use
# pyright: basic
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from runway.core.components import DeployEnvironment
from runway.module.cloudformation import CloudFormation

from ..factories import MockRunwayContext

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


class TestCloudFormation:
    """Test runway.module.cloudformation.CloudFormation."""

    @property
    def generic_parameters(self) -> Dict[str, Any]:
        """Return generic module options."""
        return {"test_key": "test-value"}

    @staticmethod
    def get_context(name: str = "test", region: str = "us-east-1") -> MockRunwayContext:
        """Create a basic Runway context object."""
        context = MockRunwayContext(
            deploy_environment=DeployEnvironment(explicit_name=name)
        )
        context.env.aws_region = region
        return context

    def test_deploy(self, tmp_path: Path, mocker: MockerFixture) -> None:
        """Test deploy."""
        mock_action = mocker.patch("runway.cfngin.cfngin.CFNgin.deploy")
        module = CloudFormation(
            self.get_context(), module_root=tmp_path, parameters=self.generic_parameters
        )
        module.deploy()
        mock_action.assert_called_once()

    def test_destroy(self, tmp_path: Path, mocker: MockerFixture) -> None:
        """Test destroy."""
        mock_action = mocker.patch("runway.cfngin.cfngin.CFNgin.destroy")
        module = CloudFormation(
            self.get_context(), module_root=tmp_path, parameters=self.generic_parameters
        )
        module.destroy()
        mock_action.assert_called_once()

    def test_plan(self, tmp_path: Path, mocker: MockerFixture) -> None:
        """Test plan."""
        mock_action = mocker.patch("runway.cfngin.cfngin.CFNgin.plan")
        module = CloudFormation(
            self.get_context(), module_root=tmp_path, parameters=self.generic_parameters
        )
        module.plan()
        mock_action.assert_called_once()
