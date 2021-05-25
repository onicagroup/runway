"""Test migrating local backend to s3."""
# pylint: disable=redefined-outer-name,unused-argument
from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Generator, cast

import pytest

from runway._cli import cli
from runway.env_mgr.tfenv import TF_VERSION_FILENAME

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest
    from click.testing import CliRunner, Result

CURRENT_DIR = Path(__file__).parent


@pytest.fixture(autouse=True, scope="module")
def tf_state_bucket(cli_runner: CliRunner) -> None:
    """Create Terraform state bucket and table."""
    cli_runner.invoke(cli, ["deploy", "--tag", "bootstrap"], env={"CI": "1"})
    yield
    destroy_result = cli_runner.invoke(
        cli, ["destroy", "--tag", "cleanup"], env={"CI": "1"}
    )
    assert destroy_result.exit_code == 0


@pytest.fixture(
    autouse=True,
    # TODO add 0.15 after implimenting https://github.com/onicagroup/runway/issues/597
    params=["0.11.15", "0.12.31", "0.13.7", "0.14.11"],
    scope="module",
)
def tf_version(request: SubRequest) -> Generator[str, None, None]:
    """Set Terraform version."""
    file_path = CURRENT_DIR / TF_VERSION_FILENAME
    file_path.write_text(cast(str, request.param) + "\n")
    yield cast(str, request.param)
    file_path.unlink(missing_ok=True)


@pytest.fixture(scope="function")
def deploy_local_backend_result(
    cli_runner: CliRunner, local_backend: Path
) -> Generator[Result, None, None]:
    """Execute `runway deploy` with `runway destory` as a cleanup step."""
    yield cli_runner.invoke(cli, ["deploy", "--tag", "local"], env={"CI": "1"})


@pytest.fixture(scope="function")
def deploy_s3_backend_result(
    cli_runner: CliRunner, s3_backend: Path
) -> Generator[Result, None, None]:
    """Execute `runway deploy` with `runway destory` as a cleanup step."""
    yield cli_runner.invoke(cli, ["deploy", "--tag", "test"], env={"CI": "1"})
    # cleanup files
    shutil.rmtree(CURRENT_DIR / ".terraform", ignore_errors=True)
    shutil.rmtree(CURRENT_DIR / "terraform.tfstate.d", ignore_errors=True)
    (CURRENT_DIR / "local_backend").unlink(missing_ok=True)
    (CURRENT_DIR / ".terraform.lock.hcl").unlink(missing_ok=True)


def test_deploy_local_backend_result(deploy_local_backend_result: Result) -> None:
    """Test deploy local backend result."""
    assert deploy_local_backend_result.exit_code == 0


@pytest.mark.order(after="test_deploy_local_backend_result")
def test_deploy_s3_backend_result(deploy_s3_backend_result: Result) -> None:
    """Test deploy s3 backend result."""
    # currently, this is expected to fail - Terraform prompts for user confirmation
    assert deploy_s3_backend_result.exit_code != 0
