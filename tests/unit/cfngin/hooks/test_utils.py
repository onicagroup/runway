"""Tests for runway.cfngin.hooks.utils."""

# pyright: reportUnknownArgumentType=none, reportUnknownVariableType=none
from __future__ import annotations

import queue
import unittest
from typing import TYPE_CHECKING, Any, ClassVar
from unittest.mock import call, patch

import pytest

from runway.cfngin.hooks.base import HookArgsBaseModel
from runway.cfngin.hooks.protocols import CfnginHookProtocol
from runway.cfngin.hooks.utils import handle_hooks
from runway.config.models.cfngin import CfnginHookDefinitionModel

from ..factories import mock_context, mock_provider

if TYPE_CHECKING:
    from unittest.mock import MagicMock

HOOK_QUEUE = queue.Queue()


class TestHooks(unittest.TestCase):
    """Tests for runway.cfngin.hooks.utils."""

    def setUp(self) -> None:
        """Run before tests."""
        self.context = mock_context(namespace="namespace")
        self.provider = mock_provider(region="us-east-1")

    def test_empty_hook_stage(self) -> None:
        """Test empty hook stage."""
        hooks = []
        handle_hooks("fake", hooks, self.provider, self.context)
        assert HOOK_QUEUE.empty()

    def test_missing_required_hook(self) -> None:
        """Test missing required hook."""
        hooks = [CfnginHookDefinitionModel(path="not.a.real.path", required=True)]
        with pytest.raises(ImportError):
            handle_hooks("missing", hooks, self.provider, self.context)

    def test_missing_required_hook_method(self) -> None:
        """Test missing required hook method."""
        with pytest.raises(AttributeError):
            handle_hooks(
                "missing",
                [CfnginHookDefinitionModel(path="runway.cfngin.hooks.blah", required=True)],
                self.provider,
                self.context,
            )

    def test_missing_non_required_hook_method(self) -> None:
        """Test missing non required hook method."""
        hooks = [CfnginHookDefinitionModel(path="runway.cfngin.hooks.blah", required=False)]
        handle_hooks("missing", hooks, self.provider, self.context)
        assert HOOK_QUEUE.empty()

    def test_default_required_hook(self) -> None:
        """Test default required hook."""
        hooks = [CfnginHookDefinitionModel(path="runway.cfngin.hooks.blah")]
        with pytest.raises(AttributeError):
            handle_hooks("missing", hooks, self.provider, self.context)

    @patch("runway.cfngin.hooks.utils.load_object_from_string")
    def test_valid_hook(self, mock_load: MagicMock) -> None:
        """Test valid hook."""
        mock_load.side_effect = [mock_hook, MockHook]
        hooks = [
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.mock_hook",
                required=True,
            ),
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.MockHook",
                required=True,
            ),
        ]
        handle_hooks("pre_deploy", hooks, self.provider, self.context)
        assert mock_load.call_count == 2
        mock_load.assert_has_calls(
            [call(hooks[0].path, try_reload=True), call(hooks[1].path, try_reload=True)]
        )
        good = HOOK_QUEUE.get_nowait()
        assert good["provider"].region == "us-east-1"
        with pytest.raises(queue.Empty):
            HOOK_QUEUE.get_nowait()

    def test_valid_enabled_hook(self) -> None:
        """Test valid enabled hook."""
        hooks = [
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.mock_hook",
                required=True,
                enabled=True,
            )
        ]
        handle_hooks("missing", hooks, self.provider, self.context)
        good = HOOK_QUEUE.get_nowait()
        assert good["provider"].region == "us-east-1"
        with pytest.raises(queue.Empty):
            HOOK_QUEUE.get_nowait()

    def test_valid_enabled_false_hook(self) -> None:
        """Test valid enabled false hook."""
        hooks = [
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.mock_hook",
                required=True,
                enabled=False,
            )
        ]
        handle_hooks("missing", hooks, self.provider, self.context)
        assert HOOK_QUEUE.empty()

    def test_context_provided_to_hook(self) -> None:
        """Test context provided to hook."""
        hooks = [
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.context_hook",
                required=True,
            )
        ]
        handle_hooks("missing", hooks, self.provider, self.context)

    def test_hook_failure(self) -> None:
        """Test hook failure."""
        hooks = [
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.fail_hook",
                required=True,
            )
        ]
        with pytest.raises(SystemExit):
            handle_hooks("fail", hooks, self.provider, self.context)
        hooks = [
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.exception_hook",
                required=True,
            )
        ]
        with pytest.raises(Exception):  # noqa: B017, PT011
            handle_hooks("fail", hooks, self.provider, self.context)
        hooks = [
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.exception_hook",
                required=False,
            )
        ]
        # Should pass
        handle_hooks("ignore_exception", hooks, self.provider, self.context)

    def test_return_data_hook(self) -> None:
        """Test return data hook."""
        hooks = [
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.result_hook",
                data_key="my_hook_results",
            ),
            # Shouldn't return data
            CfnginHookDefinitionModel(path="tests.unit.cfngin.hooks.test_utils.context_hook"),
        ]
        handle_hooks("result", hooks, self.provider, self.context)

        assert self.context.hook_data["my_hook_results"]["foo"] == "bar"
        # Verify only the first hook resulted in stored data
        assert list(self.context.hook_data.keys()) == ["my_hook_results"]

    def test_return_data_hook_duplicate_key(self) -> None:
        """Test return data hook duplicate key."""
        hooks = [
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.result_hook",
                data_key="my_hook_results",
            ),
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.result_hook",
                data_key="my_hook_results",
            ),
        ]

        with pytest.raises(KeyError):
            handle_hooks("result", hooks, self.provider, self.context)

    def test_resolve_lookups_in_args(self) -> None:
        """Test the resolution of lookups in hook args."""
        hooks = [
            CfnginHookDefinitionModel(
                path="tests.unit.cfngin.hooks.test_utils.kwargs_hook",
                data_key="my_hook_results",
                args={"default_lookup": "${default env_var::default_value}"},
            )
        ]
        handle_hooks("lookups", hooks, self.provider, self.context)

        assert self.context.hook_data["my_hook_results"]["default_lookup"] == "default_value"


class MockHook(CfnginHookProtocol):
    """Mock hook class."""

    ARGS_PARSER: ClassVar[type[HookArgsBaseModel]] = HookArgsBaseModel

    args: dict[str, Any]

    def __init__(self, **_kwargs: Any) -> None:
        """Instantiate class."""
        self.args = {}  # type: ignore

    def post_deploy(self) -> dict[str, str]:
        """Run during the **post_deploy** stage."""
        return {"status": "success"}

    def post_destroy(self) -> dict[str, str]:
        """Run during the **post_destroy** stage."""
        return {"status": "success"}

    def pre_deploy(self) -> dict[str, str]:
        """Run during the **pre_deploy** stage."""
        return {"status": "success"}

    def pre_destroy(self) -> dict[str, str]:
        """Run during the **pre_destroy** stage."""
        return {"status": "success"}


def mock_hook(*_args: Any, **kwargs: Any) -> bool:
    """Mock hook."""
    HOOK_QUEUE.put(kwargs)
    return True


def fail_hook(*_args: Any, **_kwargs: Any) -> None:
    """Fail hook."""
    return


def exception_hook(*_args: Any, **_kwargs: Any) -> None:
    """Exception hook."""
    raise Exception


def context_hook(*_args: Any, **kwargs: Any) -> bool:
    """Context hook."""
    return "context" in kwargs


def result_hook(*_args: Any, **_kwargs: Any) -> dict[str, str]:
    """Results hook."""
    return {"foo": "bar"}


def kwargs_hook(*_args: Any, **kwargs: Any) -> Any:
    """Kwargs hook."""
    return kwargs
