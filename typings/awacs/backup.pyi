"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Backup"
prefix = "backup"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CopyIntoBackupVault = Action("CopyIntoBackupVault")
CreateBackupPlan = Action("CreateBackupPlan")
CreateBackupSelection = Action("CreateBackupSelection")
CreateBackupVault = Action("CreateBackupVault")
DeleteBackupPlan = Action("DeleteBackupPlan")
DeleteBackupSelection = Action("DeleteBackupSelection")
DeleteBackupVault = Action("DeleteBackupVault")
DeleteBackupVaultAccessPolicy = Action("DeleteBackupVaultAccessPolicy")
DeleteBackupVaultNotifications = Action("DeleteBackupVaultNotifications")
DeleteRecoveryPoint = Action("DeleteRecoveryPoint")
DescribeBackupJob = Action("DescribeBackupJob")
DescribeBackupVault = Action("DescribeBackupVault")
DescribeCopyJob = Action("DescribeCopyJob")
DescribeProtectedResource = Action("DescribeProtectedResource")
DescribeRecoveryPoint = Action("DescribeRecoveryPoint")
DescribeRegionSettings = Action("DescribeRegionSettings")
DescribeRestoreJob = Action("DescribeRestoreJob")
ExportBackupPlanTemplate = Action("ExportBackupPlanTemplate")
GetBackupPlan = Action("GetBackupPlan")
GetBackupPlanFromJSON = Action("GetBackupPlanFromJSON")
GetBackupPlanFromTemplate = Action("GetBackupPlanFromTemplate")
GetBackupSelection = Action("GetBackupSelection")
GetBackupVaultAccessPolicy = Action("GetBackupVaultAccessPolicy")
GetBackupVaultNotifications = Action("GetBackupVaultNotifications")
GetRecoveryPointRestoreMetadata = Action("GetRecoveryPointRestoreMetadata")
GetSupportedResourceTypes = Action("GetSupportedResourceTypes")
ListBackupJobs = Action("ListBackupJobs")
ListBackupPlanTemplates = Action("ListBackupPlanTemplates")
ListBackupPlanVersions = Action("ListBackupPlanVersions")
ListBackupPlans = Action("ListBackupPlans")
ListBackupSelections = Action("ListBackupSelections")
ListBackupVaults = Action("ListBackupVaults")
ListCopyJobs = Action("ListCopyJobs")
ListProtectedResources = Action("ListProtectedResources")
ListRecoveryPointsByBackupVault = Action("ListRecoveryPointsByBackupVault")
ListRecoveryPointsByResource = Action("ListRecoveryPointsByResource")
ListRestoreJobs = Action("ListRestoreJobs")
ListTags = Action("ListTags")
PutBackupVaultAccessPolicy = Action("PutBackupVaultAccessPolicy")
PutBackupVaultNotifications = Action("PutBackupVaultNotifications")
StartBackupJob = Action("StartBackupJob")
StartCopyJob = Action("StartCopyJob")
StartRestoreJob = Action("StartRestoreJob")
StopBackupJob = Action("StopBackupJob")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateBackupPlan = Action("UpdateBackupPlan")
UpdateRecoveryPointLifecycle = Action("UpdateRecoveryPointLifecycle")
UpdateRegionSettings = Action("UpdateRegionSettings")
