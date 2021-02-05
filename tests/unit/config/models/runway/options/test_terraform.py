"""Test runway.config.models.runway.options.terraform."""
# pylint: disable=no-self-use
import pytest
from pydantic import ValidationError

from runway.config.models.runway.options.terraform import (
    RunwayTerraformArgsDataModel,
    RunwayTerraformBackendConfigDataModel,
    RunwayTerraformModuleOptionsDataModel,
)


class TestRunwayTerraformArgsDataModel:
    """Test RunwayTerraformArgsDataModel."""

    def test_init_default(self) -> None:
        """Test init default."""
        obj = RunwayTerraformArgsDataModel()
        assert obj.apply == []
        assert obj.init == []
        assert obj.plan == []

    def test_init_extra(self) -> None:
        """Test init extra."""
        with pytest.raises(ValidationError):
            RunwayTerraformArgsDataModel(invalid="val")

    def test_init(self) -> None:
        """Test init."""
        obj = RunwayTerraformArgsDataModel(
            apply=["-apply"], init=["-init"], plan=["-plan"]
        )
        assert obj.apply == ["-apply"]
        assert obj.init == ["-init"]
        assert obj.plan == ["-plan"]


class TestRunwayTerraformBackendConfigDataModel:
    """Test RunwayTerraformBackendConfigDataModel."""

    def test_bool(self) -> None:
        """Test __bool__."""
        assert RunwayTerraformBackendConfigDataModel(bucket="test")
        assert RunwayTerraformBackendConfigDataModel(dynamodb_table="test")
        assert RunwayTerraformBackendConfigDataModel(
            bucket="test", dynamodb_table="test"
        )
        assert not RunwayTerraformBackendConfigDataModel(region="us-east-1")
        assert not RunwayTerraformBackendConfigDataModel()

    def test_init_default(self) -> None:
        """Test init default."""
        obj = RunwayTerraformBackendConfigDataModel()
        assert not obj.bucket
        assert not obj.dynamodb_table
        assert not obj.region

    def test_init_extra(self) -> None:
        """Test init extra."""
        with pytest.raises(ValidationError):
            RunwayTerraformBackendConfigDataModel(invalid="val")

    def test_init(self) -> None:
        """Test init."""
        data = {
            "bucket": "test-bucket",
            "dynamodb_table": "test-table",
            "region": "us-east-1",
        }
        obj = RunwayTerraformBackendConfigDataModel.parse_obj(data)
        assert obj.bucket == data["bucket"]
        assert obj.dynamodb_table == data["dynamodb_table"]
        assert obj.region == data["region"]


class TestRunwayTerraformModuleOptionsDataModel:
    """Test RunwayTerraformModuleOptionsDataModel."""

    def test_convert_args(self) -> None:
        """Test _convert_args."""
        obj = RunwayTerraformModuleOptionsDataModel(args=["test"])
        assert obj.args.apply == ["test"]
        assert obj.args.init == []
        assert obj.args.plan == []

    def test_init_default(self) -> None:
        """Test init default."""
        obj = RunwayTerraformModuleOptionsDataModel()
        assert not obj.args.apply
        assert not obj.args.init
        assert not obj.args.plan
        assert not obj.backend_config
        assert not obj.version
        assert not obj.workspace
        assert not obj.write_auto_tfvars

    def test_init_extra(self) -> None:
        """Test init extra."""
        assert RunwayTerraformModuleOptionsDataModel(invalid="val")

    def test_init(self) -> None:
        """Test init."""
        data = {
            "args": {"init": ["-init"]},
            "terraform_backend_config": {"bucket": "test-bucket"},
            "terraform_version": "0.14.0",
            "terraform_workspace": "default",
            "terraform_write_auto_tfvars": True,
        }
        obj = RunwayTerraformModuleOptionsDataModel.parse_obj(data)
        assert obj.args.init == data["args"]["init"]
        assert obj.backend_config.bucket == data["terraform_backend_config"]["bucket"]
        assert obj.version == data["terraform_version"]
        assert obj.workspace == data["terraform_workspace"]
        assert obj.write_auto_tfvars == data["terraform_write_auto_tfvars"]
