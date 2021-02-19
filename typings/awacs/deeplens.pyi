"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS DeepLens"
prefix = "deeplens"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

AssociateServiceRoleToAccount = Action("AssociateServiceRoleToAccount")
BatchGetDevice = Action("BatchGetDevice")
BatchGetModel = Action("BatchGetModel")
BatchGetProject = Action("BatchGetProject")
CreateDeviceCertificates = Action("CreateDeviceCertificates")
CreateModel = Action("CreateModel")
CreateProject = Action("CreateProject")
DeleteModel = Action("DeleteModel")
DeleteProject = Action("DeleteProject")
DeployProject = Action("DeployProject")
DeregisterDevice = Action("DeregisterDevice")
GetAssociatedResources = Action("GetAssociatedResources")
GetDeploymentStatus = Action("GetDeploymentStatus")
GetDevice = Action("GetDevice")
GetModel = Action("GetModel")
GetProject = Action("GetProject")
ImportProjectFromTemplate = Action("ImportProjectFromTemplate")
ListDeployments = Action("ListDeployments")
ListDevices = Action("ListDevices")
ListModels = Action("ListModels")
ListProjects = Action("ListProjects")
RegisterDevice = Action("RegisterDevice")
RemoveProject = Action("RemoveProject")
UpdateProject = Action("UpdateProject")
