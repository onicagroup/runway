"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon CloudWatch Synthetics"
prefix = "synthetics"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateCanary = Action("CreateCanary")
DeleteCanary = Action("DeleteCanary")
DescribeCanaries = Action("DescribeCanaries")
DescribeCanariesLastRun = Action("DescribeCanariesLastRun")
GetCanaryRuns = Action("GetCanaryRuns")
ListTagsForResource = Action("ListTagsForResource")
StartCanary = Action("StartCanary")
StopCanary = Action("StopCanary")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateCanary = Action("UpdateCanary")
