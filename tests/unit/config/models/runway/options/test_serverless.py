"""Test runway.config.models.runway.options.serverless."""
# pylint: disable=no-self-use
# pyright: basic
import pytest
from pydantic import ValidationError

from runway.config.models.runway.options.serverless import (
    RunwayServerlessModuleOptionsDataModel,
    RunwayServerlessPromotezipOptionDataModel,
)


class TestRunwayServerlessModuleOptionsDataModel:
    """Test RunwayServerlessModuleOptionsDataModel."""

    def test_init_default(self) -> None:
        """Test init default values."""
        obj = RunwayServerlessModuleOptionsDataModel()
        assert obj.args == []
        assert obj.extend_serverless_yml == {}
        assert obj.promotezip == RunwayServerlessPromotezipOptionDataModel()
        assert obj.skip_npm_ci is False

    def test_init(self) -> None:
        """Test init."""
        data = {
            "args": ["--test"],
            "extend_serverless_yml": {"key": "val"},
            "promotezip": {"bucketname": "test"},
            "skip_npm_ci": True,
        }
        obj = RunwayServerlessModuleOptionsDataModel(**data)
        assert obj.args == data["args"]
        assert obj.extend_serverless_yml == data["extend_serverless_yml"]
        assert obj.promotezip == RunwayServerlessPromotezipOptionDataModel(
            **data["promotezip"]  # type: ignore
        )
        assert obj.skip_npm_ci == data["skip_npm_ci"]


class TestRunwayServerlessPromotezipOptionDataModel:
    """Test RunwayServerlessPromotezipOptionDataModel."""

    def test_bool(self) -> None:
        """Test __bool__."""
        assert RunwayServerlessPromotezipOptionDataModel(bucketname="test")
        assert not RunwayServerlessPromotezipOptionDataModel()

    def test_init_default(self) -> None:
        """Test init default."""
        obj = RunwayServerlessPromotezipOptionDataModel()
        assert obj.bucketname is None

    def test_init_extra(self) -> None:
        """Test init with extra values."""
        with pytest.raises(ValidationError):
            RunwayServerlessPromotezipOptionDataModel(invalid="something")

    def test_init(self) -> None:
        """Test init."""
        obj = RunwayServerlessPromotezipOptionDataModel(bucketname="test")
        assert obj.bucketname == "test"
