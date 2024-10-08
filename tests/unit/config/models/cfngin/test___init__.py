"""Test runway.config.models.cfngin.__init__."""

import platform
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from runway.config.models.cfngin import (
    CfnginConfigDefinitionModel,
    CfnginHookDefinitionModel,
    CfnginPackageSourcesDefinitionModel,
    CfnginStackDefinitionModel,
)


class TestCfnginConfigDefinitionModel:
    """Test runway.config.models.cfngin.CfnginConfigDefinitionModel."""

    @pytest.mark.parametrize("field", ["post_deploy", "post_destroy", "pre_deploy", "pre_destroy"])
    def test_convert_hook_definitions(self, field: str) -> None:
        """Test _convert_hook_definitions."""
        dict_hook = {"name": {"path": "something"}}
        list_hook = [{"path": "something"}]
        assert (
            CfnginConfigDefinitionModel.model_validate(
                {"namespace": "test", field: dict_hook}
            ).model_dump(exclude_unset=True)[field]
            == list_hook
        )
        assert (
            CfnginConfigDefinitionModel.model_validate(
                {"namespace": "test", field: list_hook}
            ).model_dump(exclude_unset=True)[field]
            == list_hook
        )

    def test_convert_stack_definitions(self) -> None:
        """Test _convert_stack_definitions."""
        dict_stack = {"stack-name": {"class_path": "something"}}
        list_stack = [{"class_path": "something", "name": "stack-name"}]
        assert (
            CfnginConfigDefinitionModel(
                namespace="test",
                stacks=dict_stack,  # type: ignore
            ).model_dump(exclude_unset=True)["stacks"]
            == list_stack
        )
        assert (
            CfnginConfigDefinitionModel(
                namespace="test",
                stacks=list_stack,  # type: ignore
            ).model_dump(exclude_unset=True)["stacks"]
            == list_stack
        )

    def test_extra(self) -> None:
        """Test extra fields."""
        assert (
            CfnginConfigDefinitionModel(
                common="something",  # type: ignore
                namespace="test",
            ).namespace
            == "test"
        )

    def test_field_defaults(self) -> None:
        """Test field default values."""
        obj = CfnginConfigDefinitionModel(namespace="test")
        assert not obj.cfngin_bucket
        assert not obj.cfngin_bucket_region
        assert not obj.cfngin_cache_dir
        assert obj.log_formats == {}
        assert obj.lookups == {}
        assert obj.mappings == {}
        assert obj.namespace == "test"
        assert obj.namespace_delimiter == "-"
        assert obj.package_sources == CfnginPackageSourcesDefinitionModel()
        assert not obj.persistent_graph_key
        assert obj.post_deploy == []
        assert obj.post_destroy == []
        assert obj.pre_deploy == []
        assert obj.pre_destroy == []
        assert not obj.service_role
        assert obj.stacks == []
        assert not obj.sys_path
        assert not obj.tags

    def test_parse_file(self, tmp_path: Path) -> None:
        """Test parse_file."""
        config_yml = tmp_path / "config.yml"
        config_yml.write_text(yaml.dump({"namespace": "test"}))

        obj = CfnginConfigDefinitionModel.parse_file(config_yml)
        assert obj.namespace == "test"

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="known bug where non-absolute path is returned from `.resolve()` on Windows "
        "- https://bugs.python.org/issue38671",
    )
    def test_resolve_path_fields(self) -> None:
        """Test _resolve_path_fields."""
        obj = CfnginConfigDefinitionModel(
            namespace="test",
            cfngin_cache_dir="./cache",  # type: ignore
            sys_path="./something",  # type: ignore
        )
        assert obj.cfngin_cache_dir
        assert obj.cfngin_cache_dir.is_absolute()
        assert obj.sys_path
        assert obj.sys_path.is_absolute()

    def test_required_fields(self) -> None:
        """Test required fields."""
        with pytest.raises(ValidationError, match="namespace\n  Field required"):
            CfnginConfigDefinitionModel.model_validate({})

    def test_validate_unique_stack_names(self) -> None:
        """Test _validate_unique_stack_names."""
        data = {
            "namespace": "test",
            "stacks": [
                {"name": "stack0", "class_path": "stack0"},
                {"name": "stack1", "class_path": "stack1"},
            ],
        }
        assert CfnginConfigDefinitionModel.model_validate(data)

    def test_validate_unique_stack_names_invalid(self) -> None:
        """Test _validate_unique_stack_names."""
        with pytest.raises(
            ValidationError, match="stacks\n  Value error, Duplicate stack stack0 found at index 0"
        ):
            CfnginConfigDefinitionModel.model_validate(
                {
                    "namespace": "test",
                    "stacks": [
                        {"name": "stack0", "class_path": "stack0"},
                        {"name": "stack0", "class_path": "stack0"},
                    ],
                }
            )


class TestCfnginHookDefinitionModel:
    """Test runway.config.models.cfngin.CfnginHookDefinitionModel."""

    def test_extra(self) -> None:
        """Test extra fields."""
        with pytest.raises(ValidationError, match="invalid\n  Extra inputs are not permitted"):
            CfnginHookDefinitionModel(
                invalid="something",  # type: ignore
                path="something",
            )

    def test_field_defaults(self) -> None:
        """Test field default values."""
        obj = CfnginHookDefinitionModel(path="something")
        assert obj.args == {}
        assert not obj.data_key
        assert obj.enabled
        assert obj.path == "something"
        assert obj.required

    def test_required_fields(self) -> None:
        """Test required fields."""
        with pytest.raises(ValidationError, match="path\n  Field required"):
            CfnginHookDefinitionModel.model_validate({})


class TestCfnginStackDefinitionModel:
    """Test runway.config.models.cfngin.CfnginStackDefinitionModel."""

    def test_extra(self) -> None:
        """Test extra fields."""
        with pytest.raises(ValidationError, match="invalid\n  Extra inputs are not permitted"):
            CfnginStackDefinitionModel(
                class_path="something",
                invalid="something",  # type: ignore
                name="stack-name",
            )

    def test_field_defaults(self) -> None:
        """Test field default values."""
        obj = CfnginStackDefinitionModel(class_path="something", name="stack-name")
        assert obj.class_path == "something"
        assert not obj.description
        assert obj.enabled
        assert not obj.in_progress_behavior
        assert not obj.locked
        assert obj.name == "stack-name"
        assert not obj.protected
        assert obj.required_by == []
        assert obj.requires == []
        assert not obj.stack_name
        assert not obj.stack_policy_path
        assert obj.tags == {}
        assert not obj.template_path
        assert not obj.termination_protection
        assert not obj.timeout
        assert obj.variables == {}

    def test_required_fields(self) -> None:
        """Test required fields."""
        with pytest.raises(
            ValidationError, match="Value error, either class_path or template_path must be defined"
        ):
            CfnginStackDefinitionModel.model_validate({})

    @pytest.mark.skipif(
        platform.system() == "Windows",
        reason="known bug where non-absolute path is returned from `.resolve()` on Windows "
        "- https://bugs.python.org/issue38671",
    )
    def test_resolve_path_fields(self) -> None:
        """Test _resolve_path_fields."""
        obj = CfnginStackDefinitionModel(
            name="test-stack",
            stack_policy_path="./policy.json",  # type: ignore
            template_path="./template.yml",  # type: ignore
        )
        assert obj.stack_policy_path.is_absolute()  # type: ignore
        assert obj.template_path.is_absolute()  # type: ignore

    def test_required_fields_w_class_path(self) -> None:
        """Test required fields."""
        with pytest.raises(ValidationError, match="name\n  Field required"):
            CfnginStackDefinitionModel.model_validate({"class_path": "something"})

    def test_validate_class_and_template(self) -> None:
        """Test _validate_class_and_template."""
        with pytest.raises(
            ValidationError,
            match="Value error, only one of class_path or template_path can be defined",
        ):
            CfnginStackDefinitionModel(
                class_path="something",
                name="stack-name",
                template_path="./something.yml",  # type: ignore
            )

    @pytest.mark.parametrize("enabled, locked", [(True, True), (False, True), (False, False)])
    def test_validate_class_or_template(self, enabled: bool, locked: bool) -> None:
        """Test _validate_class_or_template."""
        assert CfnginStackDefinitionModel(
            class_path="something", enabled=enabled, locked=locked, name="test-stack"
        )
        assert CfnginStackDefinitionModel(
            enabled=enabled,
            locked=locked,
            name="test-stack",
            template_path="./something.yml",  # type: ignore
        )

    def test_validate_class_or_template_invalid(self) -> None:
        """Test _validate_class_or_template invalid."""
        with pytest.raises(
            ValidationError, match="Value error, either class_path or template_path must be defined"
        ):
            CfnginStackDefinitionModel(enabled=True, locked=False, name="stack-name")
