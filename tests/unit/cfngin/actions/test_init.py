"""Test runway.cfngin.actions.init."""
# pylint: disable=no-self-use
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from mock import Mock

from runway._logging import LogLevels
from runway.cfngin.actions.init import Action
from runway.cfngin.exceptions import CfnginBucketAccessDenied, CfnginBucketRequired
from runway.config.models.cfngin import CfnginStackDefinitionModel

if TYPE_CHECKING:
    from pytest import LogCaptureFixture
    from pytest_mock import MockerFixture

    from runway.context import CfnginContext

MODULE = "runway.cfngin.actions.init"


class TestAction:
    """Test Action."""

    def test___init__(
        self, cfngin_context: CfnginContext, mocker: MockerFixture
    ) -> None:
        """Test __init__."""
        copied_context = mocker.patch.object(cfngin_context, "copy")
        obj = Action(cfngin_context)
        copied_context.assert_called_once_with()
        assert obj.context == copied_context.return_value

    def test__stack_action(self, cfngin_context: CfnginContext) -> None:
        """Test _stack_action."""
        # pylint: disable=protected-access
        assert Action(cfngin_context)._stack_action is None

    def test_cfngin_bucket(
        self, cfngin_context: CfnginContext, mocker: MockerFixture
    ) -> None:
        """Test cfngin_bucket."""
        mocker.patch.object(cfngin_context, "copy", return_value=cfngin_context)
        mocker.patch.object(cfngin_context, "s3_client")
        bucket = mocker.patch(f"{MODULE}.Bucket")
        bucket_name = mocker.patch.object(cfngin_context, "bucket_name", "bucket_name")
        bucket_region = mocker.patch.object(
            cfngin_context, "bucket_region", "bucket_region"
        )
        obj = Action(cfngin_context)
        assert obj.cfngin_bucket == bucket.return_value
        bucket.assert_called_once_with(
            cfngin_context, name=bucket_name, region=bucket_region
        )

    def test_cfngin_bucket_raise_cfngin_bucket_required(
        self, cfngin_context: CfnginContext, mocker: MockerFixture
    ) -> None:
        """Test cfngin_bucket."""
        mocker.patch.object(cfngin_context, "copy", return_value=cfngin_context)
        mocker.patch.object(cfngin_context, "s3_client")
        bucket = mocker.patch(f"{MODULE}.Bucket")
        mocker.patch.object(cfngin_context, "bucket_name", None)
        mocker.patch.object(cfngin_context, "bucket_region", "bucket_region")
        with pytest.raises(CfnginBucketRequired):
            assert not Action(cfngin_context).cfngin_bucket
        bucket.assert_not_called()

    def test_default_cfngin_bucket_stack(
        self, cfngin_context: CfnginContext, mocker: MockerFixture
    ) -> None:
        """Test default_cfngin_bucket_stack."""
        mocker.patch.object(cfngin_context, "copy", return_value=cfngin_context)
        bucket_name = mocker.patch.object(cfngin_context, "bucket_name", "bucket_name")
        assert Action(
            cfngin_context
        ).default_cfngin_bucket_stack == CfnginStackDefinitionModel(
            class_path="runway.cfngin.blueprints.cfngin_bucket.CfnginBucket",
            in_progress_behavior="wait",
            name="cfngin-bucket",
            termination_protection=True,
            variables={"BucketName": bucket_name},
        )

    def test_run(
        self,
        caplog: LogCaptureFixture,
        cfngin_context: CfnginContext,
        mocker: MockerFixture,
    ) -> None:
        """Test run."""
        caplog.set_level(LogLevels.NOTICE, logger=MODULE)
        cancel = Mock()
        mock_deploy = mocker.patch(f"{MODULE}.deploy")
        provider_builder = Mock()
        mocker.patch.object(cfngin_context, "copy", return_value=cfngin_context)
        mocker.patch.object(cfngin_context, "get_stack", return_value=None)
        mocker.patch.object(
            Action, "cfngin_bucket", Mock(exists=False, forbidden=False)
        )
        obj = Action(cfngin_context, provider_builder, cancel)
        assert not obj.run(concurrency=3, tail=True, upload_disabled=False)
        assert "using default blueprint to create cfngin_bucket..." in caplog.messages
        assert cfngin_context.config.stacks == [obj.default_cfngin_bucket_stack]
        mock_deploy.Action.assert_called_once_with(
            context=cfngin_context, provider_builder=provider_builder, cancel=cancel
        )
        mock_deploy.Action.return_value.run.assert_called_once_with(
            concurrency=3,
            tail=True,
            upload_disabled=True,
        )

    def test_run_exists(
        self,
        caplog: LogCaptureFixture,
        cfngin_context: CfnginContext,
        mocker: MockerFixture,
    ) -> None:
        """Test run."""
        caplog.set_level(LogLevels.INFO, logger=MODULE)
        cfngin_bucket = mocker.patch.object(
            Action, "cfngin_bucket", Mock(exists=True, forbidden=False, name="name")
        )
        assert not Action(cfngin_context).run()
        assert f"cfngin_bucket {cfngin_bucket.name} already exists" in caplog.messages

    def test_run_forbidden(
        self, cfngin_context: CfnginContext, mocker: MockerFixture
    ) -> None:
        """Test run."""
        mocker.patch.object(
            Action, "cfngin_bucket", Mock(forbidden=True, name="cfngin_bucket.name")
        )
        with pytest.raises(CfnginBucketAccessDenied, match="cfngin_bucket.name"):
            assert Action(cfngin_context).run()

    def test_run_get_stack(
        self,
        caplog: LogCaptureFixture,
        cfngin_context: CfnginContext,
        mocker: MockerFixture,
    ) -> None:
        """Test run."""
        caplog.set_level(LogLevels.INFO, logger=MODULE)
        cancel = Mock()
        mock_deploy = mocker.patch(f"{MODULE}.deploy")
        provider_builder = Mock()
        mocker.patch.object(cfngin_context, "copy", return_value=cfngin_context)
        get_stack = mocker.patch.object(cfngin_context, "get_stack", return_value=True)
        mocker.patch.object(
            Action, "cfngin_bucket", Mock(exists=False, forbidden=False)
        )
        assert not Action(cfngin_context, provider_builder, cancel).run()
        get_stack.assert_called_once_with("cfngin-bucket")
        assert (
            "found stack for creating cfngin_bucket: cfngin-bucket" in caplog.messages
        )
        assert cfngin_context.stack_names == ["cfngin-bucket"]
        mock_deploy.Action.assert_called_once_with(
            context=cfngin_context, provider_builder=provider_builder, cancel=cancel
        )
        mock_deploy.Action.return_value.run.assert_called_once_with(
            concurrency=0,
            tail=False,
            upload_disabled=True,
        )
