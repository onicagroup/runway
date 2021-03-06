"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon Message Delivery Service"
prefix = "ec2messages"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

AcknowledgeMessage = Action("AcknowledgeMessage")
DeleteMessage = Action("DeleteMessage")
FailMessage = Action("FailMessage")
GetEndpoint = Action("GetEndpoint")
GetMessages = Action("GetMessages")
SendReply = Action("SendReply")
