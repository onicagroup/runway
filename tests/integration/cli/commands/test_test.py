"""Test ``runway test``."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import yaml
from click.testing import CliRunner

from runway._cli import cli

SUCCESS = {
    "name": "success",
    "type": "script",
    "args": {"commands": ['echo "Hello world"']},
}
FAIL = {
    "name": "fail",
    "type": "script",
    "required": False,
    "args": {"commands": ["exit 1"]},
}
FAIL_REQUIRED = {
    "name": "fail-required",
    "type": "script",
    "required": True,
    "args": {"commands": ["exit 1"]},
}
INVALID_TYPE = {"name": "invalid-type", "type": "invalid", "required": False}
INVALID_TYPE_REQUIRED = {
    "name": "invalid-type-required",
    "type": "invalid",
    "required": True,
}

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


# def test_test_invalid_type(cd_tmp_path, capfd, caplog):
def test_test_invalid_type(
    cd_tmp_path: Path,
) -> None:  # TODO (kyle): update after catching error
    """Test ``runway test`` with two tests; one invalid."""
    # caplog.set_level(logging.INFO, logger="runway.core")
    runway_yml = cd_tmp_path / "runway.yml"
    runway_yml.write_text(
        yaml.safe_dump({"deployments": [], "tests": [INVALID_TYPE.copy(), SUCCESS.copy()]})
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["test"])
    assert result.exit_code == 1

    assert result.exception.errors()[0]["loc"] == ("tests", 0, "type")  # type: ignore


def test_test_not_defined(cd_tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test ``runway test`` with no tests defined."""
    caplog.set_level(logging.ERROR)
    runway_yml = cd_tmp_path / "runway.yml"
    runway_yml.write_text(yaml.safe_dump({"deployments": []}))

    runner = CliRunner()
    result = runner.invoke(cli, ["test"])
    assert result.exit_code == 1
    assert "no tests defined in runway.yml" in caplog.messages


def test_test_single_successful(
    cd_tmp_path: Path, capfd: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture
) -> None:
    """Test ``runway test`` with a single, successful test."""
    caplog.set_level(logging.INFO, logger="runway.core")
    runway_yml = cd_tmp_path / "runway.yml"
    runway_yml.write_text(yaml.safe_dump({"deployments": [], "tests": [SUCCESS.copy()]}))

    runner = CliRunner()
    result = runner.invoke(cli, ["test"])
    assert result.exit_code == 0

    captured = capfd.readouterr()
    logs = "\n".join(caplog.messages)
    assert "found 1 test(s)" in logs
    assert "success:running test (in progress)" in logs
    assert "Hello world" in captured.out
    assert "success:running test (pass)" in logs


def test_test_two_test(
    cd_tmp_path: Path, capfd: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture
) -> None:
    """Test ``runway test`` with two tests; one failing."""
    caplog.set_level(logging.INFO, logger="runway.core")
    runway_yml = cd_tmp_path / "runway.yml"
    runway_yml.write_text(
        yaml.safe_dump({"deployments": [], "tests": [FAIL.copy(), SUCCESS.copy()]})
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["test"])
    assert result.exit_code == 1

    captured = capfd.readouterr()
    logs = "\n".join(caplog.messages)
    assert "found 2 test(s)" in logs
    assert "fail:running test (in progress)" in logs
    assert "fail:running test (fail)" in logs
    assert "success:running test (in progress)" in logs
    assert "Hello world" in captured.out
    assert "success:running test (pass)" in logs
    assert "the following tests failed: fail" in logs


def test_test_two_test_required(
    cd_tmp_path: Path, capfd: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture
) -> None:
    """Test ``runway test`` with two tests; one failing required."""
    caplog.set_level(logging.INFO)
    runway_yml = cd_tmp_path / "runway.yml"
    runway_yml.write_text(
        yaml.safe_dump({"deployments": [], "tests": [FAIL_REQUIRED.copy(), SUCCESS.copy()]})
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["test"])
    assert result.exit_code == 1

    captured = capfd.readouterr()
    logs = "\n".join(caplog.messages)
    assert "found 2 test(s)" in logs
    assert "fail-required:running test (in progress)" in logs
    assert "fail-required:running test (fail)" in logs
    assert "fail-required:test required; the remaining tests have been skipped" in logs
    assert "success:running test (in progress)" not in logs
    assert "Hello world" not in captured.out
