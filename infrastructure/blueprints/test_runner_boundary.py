"""Blueprint for permissions boundary of the test runner user."""
# pylint: disable=no-self-use
from __future__ import annotations

from typing import Final, List

import awacs.iam
from awacs.aws import Action, Deny, Statement
from troposphere import Sub

from runway.compat import cached_property

from .prevent_privilege_escalation import AdminPreventPrivilegeEscalation


class TestRunnerBoundary(AdminPreventPrivilegeEscalation):
    """Blueprint for IAM permission boundary that prevents privilege escalation."""

    DESCRIPTION: Final[str] = "Permission boundary for the test runner user."
    POLICY_NAME: Final[str] = "TestRunnerBoundary"

    @cached_property
    def statement_deny_cloudtrail(self) -> Statement:
        """Statement to deny access to CloudTrail."""
        return Statement(
            Action=[Action("cloudtrail", "*")],
            Effect=Deny,
            Resource=["*"],
            Sid="DenyCloudTrail",
        )

    @cached_property
    def statement_deny_iam(self) -> Statement:
        """Statement to deny access to some IAM calls."""
        return Statement(
            Action=[
                awacs.iam.CreateAccessKey,
                awacs.iam.CreateAccountAlias,
                awacs.iam.CreateInstanceProfile,
                awacs.iam.CreateLoginProfile,
                awacs.iam.CreateOpenIDConnectProvider,
                awacs.iam.CreateSAMLProvider,
                awacs.iam.CreateServiceSpecificCredential,
                awacs.iam.CreateUser,
                awacs.iam.DeactivateMFADevice,
                awacs.iam.DeleteAccessKey,
                awacs.iam.DeleteAccountAlias,
                awacs.iam.DeleteAccountPasswordPolicy,
                awacs.iam.DeleteInstanceProfile,
                awacs.iam.DeleteLoginProfile,
                awacs.iam.DeleteOpenIDConnectProvider,
                awacs.iam.DeleteSAMLProvider,
                awacs.iam.DeleteSSHPublicKey,
                awacs.iam.DeleteServiceLinkedRole,
                awacs.iam.DeleteServiceSpecificCredential,
                awacs.iam.DeleteSigningCertificate,
                awacs.iam.DeleteUser,
                awacs.iam.DeleteUserPermissionsBoundary,
                awacs.iam.DeleteUserPolicy,
                awacs.iam.DeleteVirtualMFADevice,
                awacs.iam.DetachUserPolicy,
                awacs.iam.GetAccountAuthorizationDetails,
                awacs.iam.GetAccountSummary,
                awacs.iam.GetCredentialReport,
                awacs.iam.RemoveUserFromGroup,
                awacs.iam.ResetServiceSpecificCredential,
                awacs.iam.ResyncMFADevice,
                awacs.iam.SetSecurityTokenServicePreferences,
                awacs.iam.UpdateAccessKey,
                awacs.iam.UpdateAccountPasswordPolicy,
                awacs.iam.UpdateLoginProfile,
                awacs.iam.UpdateSAMLProvider,
                awacs.iam.UpdateSSHPublicKey,
                awacs.iam.UpdateServerCertificate,
                awacs.iam.UpdateServiceSpecificCredential,
                awacs.iam.UpdateSigningCertificate,
                awacs.iam.UpdateUser,
                awacs.iam.UploadSSHPublicKey,
                awacs.iam.UploadServerCertificate,
                awacs.iam.UploadSigningCertificate,
            ],
            Effect=Deny,
            Resource=["*"],
            Sid="DenyIam",
        )

    @cached_property
    def statement_deny_namespace(self) -> Statement:
        """Statement to deny access to resources in the same namespace."""
        return Statement(
            Action=[Action("*")],
            Effect=Deny,
            Resource=[
                Sub(
                    "arn:aws:cloudformation:*:${AWS::AccountId}:stack/"
                    f"{self.namespace}-*"
                ),
                Sub(f"arn:aws:s3:::${self.namespace}"),
                Sub(f"arn:aws:s3:::${self.namespace}/*"),
                Sub(f"arn:aws:s3:::${self.namespace}-*"),
                Sub(f"arn:aws:s3:::${self.namespace}-*/*"),
            ],
        )

    @cached_property
    def statements(self) -> List[Statement]:
        """List of statements to add to the policy."""
        return super().statements + [
            self.statement_deny_cloudtrail,
            self.statement_deny_iam,
            self.statement_deny_namespace,
        ]
