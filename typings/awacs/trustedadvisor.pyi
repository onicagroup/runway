"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Trusted Advisor"
prefix = "trustedadvisor"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

DescribeAccount = Action("DescribeAccount")
DescribeAccountAccess = Action("DescribeAccountAccess")
DescribeCheckItems = Action("DescribeCheckItems")
DescribeCheckRefreshStatuses = Action("DescribeCheckRefreshStatuses")
DescribeCheckSummaries = Action("DescribeCheckSummaries")
DescribeChecks = Action("DescribeChecks")
DescribeNotificationPreferences = Action("DescribeNotificationPreferences")
DescribeOrganization = Action("DescribeOrganization")
DescribeOrganizationAccounts = Action("DescribeOrganizationAccounts")
DescribeReports = Action("DescribeReports")
DescribeServiceMetadata = Action("DescribeServiceMetadata")
ExcludeCheckItems = Action("ExcludeCheckItems")
GenerateReport = Action("GenerateReport")
IncludeCheckItems = Action("IncludeCheckItems")
RefreshCheck = Action("RefreshCheck")
SetAccountAccess = Action("SetAccountAccess")
SetOrganizationAccess = Action("SetOrganizationAccess")
UpdateNotificationPreferences = Action("UpdateNotificationPreferences")
