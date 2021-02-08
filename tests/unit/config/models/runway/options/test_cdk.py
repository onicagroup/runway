"""Test runway.config.models.runway.options.cdk."""
# pylint: disable=no-self-use
from runway.config.models.runway.options.cdk import RunwayCdkModuleOptionsDataModel


class TestRunwayCdkModuleOptionsDataModel:
    """Test RunwayCdkModuleOptionsDataModel."""

    def test_init_default(self) -> None:
        """Test init default."""
        obj = RunwayCdkModuleOptionsDataModel()
        assert obj.build_steps == []
        assert not obj.skip_npm_ci

    def test_init_extra(self) -> None:
        """Test init extra."""
        obj = RunwayCdkModuleOptionsDataModel(invalid="val")
        assert "invalid" not in obj.dict()

    def test_init(self) -> None:
        """Test init."""
        obj = RunwayCdkModuleOptionsDataModel(
            build_steps=["test0", "test1"], skip_npm_ci=True
        )
        assert obj.build_steps == ["test0", "test1"]
        assert obj.skip_npm_ci
