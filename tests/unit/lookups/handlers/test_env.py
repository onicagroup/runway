"""Tests for lookup handler for env."""
# pylint: disable=no-self-use
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from runway.lookups.handlers.env import EnvLookup

if TYPE_CHECKING:
    from ...factories import MockRunwayContext

ENV_VARS = {"str_val": "test"}


class TestEnvLookup:
    """Tests for EnvLookup."""

    def test_handle(self, runway_context: MockRunwayContext) -> None:
        """Validate handle base functionality."""
        runway_context.env.vars = ENV_VARS.copy()
        result = EnvLookup.handle("str_val", context=runway_context)
        assert result == "test"

    def test_handle_not_found(self, runway_context: MockRunwayContext) -> None:
        """Validate exception when lookup cannot be resolved."""
        runway_context.env.vars = ENV_VARS.copy()
        with pytest.raises(ValueError):
            EnvLookup.handle("NOT_VALID", context=runway_context)
