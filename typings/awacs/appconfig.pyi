"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS AppConfig"
prefix = "appconfig"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateApplication = Action("CreateApplication")
CreateConfigurationProfile = Action("CreateConfigurationProfile")
CreateDeploymentStrategy = Action("CreateDeploymentStrategy")
CreateEnvironment = Action("CreateEnvironment")
CreateHostedConfigurationVersion = Action("CreateHostedConfigurationVersion")
DeleteApplication = Action("DeleteApplication")
DeleteConfigurationProfile = Action("DeleteConfigurationProfile")
DeleteDeploymentStrategy = Action("DeleteDeploymentStrategy")
DeleteEnvironment = Action("DeleteEnvironment")
DeleteHostedConfigurationVersion = Action("DeleteHostedConfigurationVersion")
GetApplication = Action("GetApplication")
GetConfiguration = Action("GetConfiguration")
GetConfigurationProfile = Action("GetConfigurationProfile")
GetDeployment = Action("GetDeployment")
GetDeploymentStrategy = Action("GetDeploymentStrategy")
GetEnvironment = Action("GetEnvironment")
GetHostedConfigurationVersion = Action("GetHostedConfigurationVersion")
ListApplications = Action("ListApplications")
ListConfigurationProfiles = Action("ListConfigurationProfiles")
ListDeploymentStrategies = Action("ListDeploymentStrategies")
ListDeployments = Action("ListDeployments")
ListEnvironments = Action("ListEnvironments")
ListHostedConfigurationVersions = Action("ListHostedConfigurationVersions")
ListTagsForResource = Action("ListTagsForResource")
StartDeployment = Action("StartDeployment")
StopDeployment = Action("StopDeployment")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateApplication = Action("UpdateApplication")
UpdateConfigurationProfile = Action("UpdateConfigurationProfile")
UpdateDeploymentStrategy = Action("UpdateDeploymentStrategy")
UpdateEnvironment = Action("UpdateEnvironment")
ValidateConfiguration = Action("ValidateConfiguration")