"""Test ``runway tfenv install`` command."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from click.testing import CliRunner

from runway._cli import cli

if TYPE_CHECKING:
    import pytest


def test_tfenv_install(cd_tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test ``runway tfenv install`` reading version from a file.

    For best results, remove any existing installs.

    """
    caplog.set_level(logging.DEBUG, logger="runway.cli.commands.tfenv")
    (cd_tmp_path / ".terraform-version").write_text("0.12.0")
    runner = CliRunner()
    result = runner.invoke(cli, ["tfenv", "install"])
    assert result.exit_code == 0

    tf_bin = Path(caplog.messages[-1].replace("terraform path: ", ""))
    assert tf_bin.exists()


def test_tfenv_install_no_version_file(
    cli_runner: CliRunner, caplog: pytest.LogCaptureFixture
) -> None:
    """Test ``runway tfenv install`` no version file."""
    caplog.set_level(logging.ERROR, logger="runway")
    assert cli_runner.invoke(cli, ["tfenv", "install"]).exit_code == 1

    assert "unable to find a .terraform-version file" in "\n".join(caplog.messages)


def test_tfenv_install_version(caplog: pytest.LogCaptureFixture) -> None:
    """Test ``runway tfenv install <version>``.

    For best results, remove any existing installs.

    """
    caplog.set_level(logging.DEBUG, logger="runway.cli.commands.tfenv")
    runner = CliRunner()
    result = runner.invoke(cli, ["tfenv", "install", "0.12.1"])
    assert result.exit_code == 0

    tf_bin = Path(caplog.messages[-1].replace("terraform path: ", ""))
    assert tf_bin.exists()
