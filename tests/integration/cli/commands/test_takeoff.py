"""Test ``runway takeoff``."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from click.testing import CliRunner
from mock import MagicMock

from runway._cli import cli
from runway._cli.commands import deploy

if TYPE_CHECKING:
    from pathlib import Path

    from pytest import LogCaptureFixture, MonkeyPatch

    from ...conftest import CpConfigTypeDef


def test_takeoff(
    caplog: LogCaptureFixture,
    cd_tmp_path: Path,
    cp_config: CpConfigTypeDef,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test takeoff."""
    cp_config("min_required", cd_tmp_path)
    caplog.set_level(logging.DEBUG, logger="runway.cli.commands.takeoff")
    mock_forward = MagicMock()
    monkeypatch.setattr("click.Context.forward", mock_forward)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "takeoff",
            "--ci",
            "--deploy-environment",
            "test",
            "--tag",
            "tag1",
            "--tag",
            "tag2",
        ],
    )
    assert result.exit_code == 0
    assert "forwarding to deploy..." in caplog.messages
    mock_forward.assert_called_once_with(
        deploy,
        ci=True,
        debug=0,
        deploy_environment="test",
        no_color=False,
        tags=("tag1", "tag2"),
        verbose=False,
    )
