"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Mobile Hub"
prefix = "mobilehub"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateProject = Action("CreateProject")
CreateServiceRole = Action("CreateServiceRole")
DeleteProject = Action("DeleteProject")
DeleteProjectSnapshot = Action("DeleteProjectSnapshot")
DeployToStage = Action("DeployToStage")
DescribeBundle = Action("DescribeBundle")
ExportBundle = Action("ExportBundle")
ExportProject = Action("ExportProject")
GenerateProjectParameters = Action("GenerateProjectParameters")
GetProject = Action("GetProject")
GetProjectSnapshot = Action("GetProjectSnapshot")
ImportProject = Action("ImportProject")
InstallBundle = Action("InstallBundle")
ListAvailableConnectors = Action("ListAvailableConnectors")
ListAvailableFeatures = Action("ListAvailableFeatures")
ListAvailableRegions = Action("ListAvailableRegions")
ListBundles = Action("ListBundles")
ListProjectSnapshots = Action("ListProjectSnapshots")
ListProjects = Action("ListProjects")
SynchronizeProject = Action("SynchronizeProject")
UpdateProject = Action("UpdateProject")
ValidateProject = Action("ValidateProject")
VerifyServiceRole = Action("VerifyServiceRole")
