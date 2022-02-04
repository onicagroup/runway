"""Tests for runway.cfngin.hooks.route53."""
from __future__ import annotations

from typing import TYPE_CHECKING

from runway.cfngin.hooks.route53 import create_domain

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

    from ...factories import MockCFNginContext

MODULE = "runway.cfngin.hooks.route53"


def test_create_domain(
    cfngin_context: MockCFNginContext, mocker: MockerFixture
) -> None:
    """Test create_domain."""
    domain = "foo"
    create_route53_zone = mocker.patch(
        f"{MODULE}.create_route53_zone", return_value="bar"
    )
    _ = cfngin_context.add_stubber("route53")
    assert create_domain(cfngin_context, domain=domain) == {
        "domain": domain,
        "zone_id": create_route53_zone.return_value,
    }
    # pylint: disable=protected-access
    create_route53_zone.assert_called_once_with(
        cfngin_context._boto3_test_client[f"route53.{cfngin_context.env.aws_region}"],
        domain,
    )
