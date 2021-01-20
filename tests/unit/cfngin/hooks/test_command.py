"""Tests for runway.cfngin.hooks.command."""
# pylint: disable=no-self-use
import os
import unittest
from subprocess import PIPE
from typing import Any, List, Optional, Tuple, Union

import mock

from runway.cfngin.hooks.command import run_command
from runway.config import CfnginConfig
from runway.context.cfngin import CfnginContext

from ..factories import mock_provider


class MockProcess:
    """Mock process."""

    def __init__(
        self,
        returncode: int = 0,
        stdout: Optional[str] = "",
        stderr: Optional[str] = "",
    ) -> None:
        """Instantiate class."""
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = None

    def communicate(self, stdin: str) -> Tuple[Optional[str], Optional[str]]:
        """Communicate with process."""
        self.stdin = stdin
        return (self.stdout, self.stderr)

    def wait(self) -> int:
        """Wait for process."""
        return self.returncode

    def kill(self) -> None:
        """Kill process."""
        return


class TestCommandHook(unittest.TestCase):
    """Tests for runway.cfngin.hooks.command."""

    def setUp(self) -> None:
        """Run before tests."""
        self.context = CfnginContext(
            config=CfnginConfig.parse_obj(
                {"namespace": "test", "cfngin_bucket": "test"}
            )
        )
        self.provider = mock_provider(region="us-east-1")

        self.mock_process = MockProcess()
        self.popen_mock = mock.patch(
            "runway.cfngin.hooks.command.Popen", return_value=self.mock_process
        ).start()

        self.devnull = mock.Mock()
        self.devnull_mock = mock.patch(
            "runway.cfngin.hooks.command._devnull", return_value=self.devnull
        ).start()

    def tearDown(self) -> None:
        """Run after tests."""
        self.devnull_mock.stop()
        self.popen_mock.stop()

    def run_hook(self, *, command: Union[str, List[str]], **kwargs: Any) -> Any:
        """Run hook."""
        real_kwargs = {
            "context": self.context,
        }
        real_kwargs.update(kwargs)
        return run_command(command=command, **real_kwargs)

    def test_command_ok(self) -> None:
        """Test command ok."""
        self.mock_process.returncode = 0
        self.mock_process.stdout = None
        self.mock_process.stderr = None

        results = self.run_hook(command=["foo"])

        self.assertEqual(results, {"returncode": 0, "stdout": None, "stderr": None})
        self.popen_mock.assert_called_once_with(
            ["foo"], stdin=self.devnull, stdout=None, stderr=None, env=None
        )

    def test_command_fail(self) -> None:
        """Test command fail."""
        self.mock_process.returncode = 1
        self.mock_process.stdout = None
        self.mock_process.stderr = None

        results = self.run_hook(command=["foo"])

        self.assertEqual(results, {})
        self.popen_mock.assert_called_once_with(
            ["foo"], stdin=self.devnull, stdout=None, stderr=None, env=None
        )

    def test_command_ignore_status(self) -> None:
        """Test command ignore status."""
        self.mock_process.returncode = 1
        self.mock_process.stdout = None
        self.mock_process.stderr = None

        results = self.run_hook(command=["foo"], ignore_status=True)

        self.assertEqual(results, {"returncode": 1, "stdout": None, "stderr": None})
        self.popen_mock.assert_called_once_with(
            ["foo"], stdin=self.devnull, stdout=None, stderr=None, env=None
        )

    def test_command_quiet(self) -> None:
        """Test command quiet."""
        self.mock_process.returncode = 0
        self.mock_process.stdout = None
        self.mock_process.stderr = None

        results = self.run_hook(command=["foo"], quiet=True)
        self.assertEqual(results, {"returncode": 0, "stdout": None, "stderr": None})

        self.popen_mock.assert_called_once_with(
            ["foo"],
            stdin=self.devnull,
            stdout=self.devnull,
            stderr=self.devnull,
            env=None,
        )

    def test_command_interactive(self) -> None:
        """Test command interactive."""
        self.mock_process.returncode = 0
        self.mock_process.stdout = None
        self.mock_process.stderr = None

        results = self.run_hook(command=["foo"], interactive=True)
        self.assertEqual(results, {"returncode": 0, "stdout": None, "stderr": None})

        self.popen_mock.assert_called_once_with(
            ["foo"], stdin=None, stdout=None, stderr=None, env=None
        )

    def test_command_input(self) -> None:
        """Test command input."""
        self.mock_process.returncode = 0
        self.mock_process.stdout = None
        self.mock_process.stderr = None

        results = self.run_hook(command=["foo"], stdin="hello world")
        self.assertEqual(results, {"returncode": 0, "stdout": None, "stderr": None})

        self.popen_mock.assert_called_once_with(
            ["foo"], stdin=PIPE, stdout=None, stderr=None, env=None
        )
        self.assertEqual(self.mock_process.stdin, "hello world")

    def test_command_capture(self) -> None:
        """Test command capture."""
        self.mock_process.returncode = 0
        self.mock_process.stdout = "hello"
        self.mock_process.stderr = "world"

        results = self.run_hook(command=["foo"], capture=True)
        self.assertEqual(
            results, {"returncode": 0, "stdout": "hello", "stderr": "world"}
        )

        self.popen_mock.assert_called_once_with(
            ["foo"], stdin=self.devnull, stdout=PIPE, stderr=PIPE, env=None
        )

    def test_command_env(self) -> None:
        """Test command env."""
        self.mock_process.returncode = 0
        self.mock_process.stdout = None
        self.mock_process.stderr = None

        with mock.patch.dict(os.environ, {"foo": "bar"}, clear=True):
            results = self.run_hook(command=["foo"], env={"hello": "world"})

            self.assertEqual(results, {"returncode": 0, "stdout": None, "stderr": None})
            self.popen_mock.assert_called_once_with(
                ["foo"],
                stdin=self.devnull,
                stdout=None,
                stderr=None,
                env={"hello": "world", "foo": "bar"},
            )
