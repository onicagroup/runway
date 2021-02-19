"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Cloud Map"
prefix = "servicediscovery"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateHttpNamespace = Action("CreateHttpNamespace")
CreatePrivateDnsNamespace = Action("CreatePrivateDnsNamespace")
CreatePublicDnsNamespace = Action("CreatePublicDnsNamespace")
CreateService = Action("CreateService")
DeleteNamespace = Action("DeleteNamespace")
DeleteService = Action("DeleteService")
DeregisterInstance = Action("DeregisterInstance")
DiscoverInstances = Action("DiscoverInstances")
GetInstance = Action("GetInstance")
GetInstancesHealthStatus = Action("GetInstancesHealthStatus")
GetNamespace = Action("GetNamespace")
GetOperation = Action("GetOperation")
GetService = Action("GetService")
ListInstances = Action("ListInstances")
ListNamespaces = Action("ListNamespaces")
ListOperations = Action("ListOperations")
ListServices = Action("ListServices")
ListTagsForResource = Action("ListTagsForResource")
RegisterInstance = Action("RegisterInstance")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateInstanceCustomHealthStatus = Action("UpdateInstanceCustomHealthStatus")
UpdateInstanceHeartbeatStatus = Action("UpdateInstanceHeartbeatStatus")
UpdateService = Action("UpdateService")
