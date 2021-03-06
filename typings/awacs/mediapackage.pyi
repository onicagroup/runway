"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Elemental MediaPackage"
prefix = "mediapackage"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateChannel = Action("CreateChannel")
CreateOriginEndpoint = Action("CreateOriginEndpoint")
DeleteChannel = Action("DeleteChannel")
DeleteOriginEndpoint = Action("DeleteOriginEndpoint")
DescribeChannel = Action("DescribeChannel")
DescribeOriginEndpoint = Action("DescribeOriginEndpoint")
ListChannels = Action("ListChannels")
ListOriginEndpoints = Action("ListOriginEndpoints")
ListTagsForResource = Action("ListTagsForResource")
RotateIngestEndpointCredentials = Action("RotateIngestEndpointCredentials")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateChannel = Action("UpdateChannel")
UpdateOriginEndpoint = Action("UpdateOriginEndpoint")
