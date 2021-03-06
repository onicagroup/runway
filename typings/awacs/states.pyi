"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Step Functions"
prefix = "states"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateActivity = Action("CreateActivity")
CreateStateMachine = Action("CreateStateMachine")
DeleteActivity = Action("DeleteActivity")
DeleteStateMachine = Action("DeleteStateMachine")
DescribeActivity = Action("DescribeActivity")
DescribeExecution = Action("DescribeExecution")
DescribeStateMachine = Action("DescribeStateMachine")
DescribeStateMachineForExecution = Action("DescribeStateMachineForExecution")
GetActivityTask = Action("GetActivityTask")
GetExecutionHistory = Action("GetExecutionHistory")
ListActivities = Action("ListActivities")
ListExecutions = Action("ListExecutions")
ListStateMachines = Action("ListStateMachines")
ListTagsForResource = Action("ListTagsForResource")
SendTaskFailure = Action("SendTaskFailure")
SendTaskHeartbeat = Action("SendTaskHeartbeat")
SendTaskSuccess = Action("SendTaskSuccess")
StartExecution = Action("StartExecution")
StopExecution = Action("StopExecution")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateStateMachine = Action("UpdateStateMachine")
