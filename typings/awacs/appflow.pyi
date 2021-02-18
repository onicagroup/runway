"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon AppFlow"
prefix = "appflow"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateConnectorProfile = Action("CreateConnectorProfile")
CreateFlow = Action("CreateFlow")
DeleteConnectorProfile = Action("DeleteConnectorProfile")
DeleteFlow = Action("DeleteFlow")
DescribeConnectorEntity = Action("DescribeConnectorEntity")
DescribeConnectorFields = Action("DescribeConnectorFields")
DescribeConnectorProfiles = Action("DescribeConnectorProfiles")
DescribeConnectors = Action("DescribeConnectors")
DescribeFlow = Action("DescribeFlow")
DescribeFlowExecution = Action("DescribeFlowExecution")
DescribeFlowExecutionRecords = Action("DescribeFlowExecutionRecords")
DescribeFlows = Action("DescribeFlows")
ListConnectorEntities = Action("ListConnectorEntities")
ListConnectorFields = Action("ListConnectorFields")
ListFlows = Action("ListFlows")
ListTagsForResource = Action("ListTagsForResource")
RunFlow = Action("RunFlow")
StartFlow = Action("StartFlow")
StopFlow = Action("StopFlow")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateConnectorProfile = Action("UpdateConnectorProfile")
UpdateFlow = Action("UpdateFlow")
