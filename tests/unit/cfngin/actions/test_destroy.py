"""Tests for runway.cfngin.actions.destroy."""
# pylint: disable=no-self-use,protected-access,unused-argument
from __future__ import annotations

import unittest
from typing import Any, Dict, Optional

from mock import MagicMock, PropertyMock, patch

from runway.cfngin.actions import destroy
from runway.cfngin.exceptions import StackDoesNotExist
from runway.cfngin.plan import Graph, Step
from runway.cfngin.status import COMPLETE, PENDING, SKIPPED, SUBMITTED
from runway.config import CfnginConfig
from runway.context.cfngin import CfnginContext

from ..factories import MockProviderBuilder, MockThreadingEvent


class MockStack:
    """Mock our local CFNgin stack and an AWS provider stack."""

    def __init__(self, name: str, tags: Any = None, **_: Any) -> None:
        """Instantiate class."""
        self.name = name
        self.fqn = name
        self.region = None
        self.profile = None
        self.requires = []


class TestDestroyAction(unittest.TestCase):
    """Tests for runway.cfngin.actions.destroy.DestroyAction."""

    def setUp(self):
        """Run before tests."""
        self.context = self._get_context()
        self.action = destroy.Action(self.context, cancel=MockThreadingEvent())  # type: ignore

    def _get_context(
        self, extra_config_args: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> CfnginContext:
        """Get context."""
        config = {
            "namespace": "namespace",
            "stacks": [
                {"name": "vpc", "template_path": "."},
                {"name": "bastion", "requires": ["vpc"], "template_path": "."},
                {
                    "name": "instance",
                    "requires": ["vpc", "bastion"],
                    "template_path": ".",
                },
                {
                    "name": "db",
                    "requires": ["instance", "vpc", "bastion"],
                    "template_path": ".",
                },
                {"name": "other", "requires": ["db"], "template_path": "."},
            ],
        }
        if extra_config_args:
            config.update(extra_config_args)
        return CfnginContext(config=CfnginConfig.parse_obj(config), **kwargs)

    def test_generate_plan(self) -> None:
        """Test generate plan."""
        plan = self.action._generate_plan(reverse=True)
        self.assertEqual(
            {
                "vpc": set(["db", "instance", "bastion"]),
                "other": set([]),
                "bastion": set(["instance", "db"]),
                "instance": set(["db"]),
                "db": set(["other"]),
            },
            plan.graph.to_dict(),
        )

    def test_only_execute_plan_when_forced(self) -> None:
        """Test only execute plan when forced."""
        with patch.object(self.action, "_generate_plan") as mock_generate_plan:
            self.action.run(force=False)
            self.assertEqual(mock_generate_plan().execute.call_count, 0)

    def test_execute_plan_when_forced(self) -> None:
        """Test execute plan when forced."""
        with patch.object(self.action, "_generate_plan") as mock_generate_plan:
            self.action.run(force=True)
            self.assertEqual(mock_generate_plan().execute.call_count, 1)

    def test_destroy_stack_complete_if_state_submitted(self) -> None:
        """Test destroy stack complete if state submitted."""
        # Simulate the provider not being able to find the stack (a result of
        # it being successfully deleted)
        provider = MagicMock()
        provider.get_stack.side_effect = StackDoesNotExist("mock")
        self.action.provider_builder = MockProviderBuilder(provider=provider)
        status = self.action._destroy_stack(MockStack("vpc"), status=PENDING)  # type: ignore
        # if we haven't processed the step (ie. has never been SUBMITTED,
        # should be skipped)
        self.assertEqual(status, SKIPPED)
        status = self.action._destroy_stack(MockStack("vpc"), status=SUBMITTED)  # type: ignore
        # if we have processed the step and then can't find the stack, it means
        # we successfully deleted it
        self.assertEqual(status, COMPLETE)

    def test_destroy_stack_step_statuses(self) -> None:
        """Test destroy stack step statuses."""
        mock_provider = MagicMock()
        stacks_dict = self.context.stacks_dict

        def get_stack(stack_name):
            return stacks_dict.get(stack_name)

        plan = self.action._generate_plan()
        step = plan.steps[0]
        # we need the AWS provider to generate the plan, but swap it for
        # the mock one to make the test easier
        self.action.provider_builder = MockProviderBuilder(provider=mock_provider)

        # simulate stack doesn't exist and we haven't submitted anything for
        # deletion
        mock_provider.get_stack.side_effect = StackDoesNotExist("mock")

        step.run()
        self.assertEqual(step.status, SKIPPED)

        # simulate stack getting successfully deleted
        mock_provider.get_stack.side_effect = get_stack
        mock_provider.is_stack_destroyed.return_value = False
        mock_provider.is_stack_in_progress.return_value = False

        step._run_once()
        self.assertEqual(step.status, SUBMITTED)
        mock_provider.is_stack_destroyed.return_value = False
        mock_provider.is_stack_in_progress.return_value = True

        step._run_once()
        self.assertEqual(step.status, SUBMITTED)
        mock_provider.is_stack_destroyed.return_value = True
        mock_provider.is_stack_in_progress.return_value = False

        step._run_once()
        self.assertEqual(step.status, COMPLETE)

    @patch(
        "runway.context.cfngin.CfnginContext.persistent_graph_tags",
        new_callable=PropertyMock,
    )
    @patch(
        "runway.context.cfngin.CfnginContext.lock_persistent_graph",
        new_callable=MagicMock,
    )
    @patch(
        "runway.context.cfngin.CfnginContext.unlock_persistent_graph",
        new_callable=MagicMock,
    )
    @patch("runway.cfngin.plan.Plan.execute", new_callable=MagicMock)
    def test_run_persist(
        self,
        mock_execute: MagicMock,
        mock_unlock: MagicMock,
        mock_lock: MagicMock,
        mock_graph_tags: PropertyMock,
    ) -> None:
        """Test run persist."""
        mock_graph_tags.return_value = {}
        context = self._get_context(
            extra_config_args={"persistent_graph_key": "test.json"}
        )
        context._persistent_graph = Graph.from_steps(
            [Step.from_stack_name("removed", context)]
        )
        destroy_action = destroy.Action(context=context)
        destroy_action.run(force=True)

        mock_graph_tags.assert_called_once()
        mock_lock.assert_called_once()
        mock_execute.assert_called_once()
        mock_unlock.assert_called_once()
