"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS IoT Events"
prefix = "iotevents"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

BatchPutMessage = Action("BatchPutMessage")
BatchUpdateDetector = Action("BatchUpdateDetector")
CreateDetectorModel = Action("CreateDetectorModel")
CreateInput = Action("CreateInput")
DeleteDetectorModel = Action("DeleteDetectorModel")
DeleteInput = Action("DeleteInput")
DescribeDetector = Action("DescribeDetector")
DescribeDetectorModel = Action("DescribeDetectorModel")
DescribeInput = Action("DescribeInput")
DescribeLoggingOptions = Action("DescribeLoggingOptions")
ListDetectorModelVersions = Action("ListDetectorModelVersions")
ListDetectorModels = Action("ListDetectorModels")
ListDetectors = Action("ListDetectors")
ListInputs = Action("ListInputs")
ListTagsForResource = Action("ListTagsForResource")
PutLoggingOptions = Action("PutLoggingOptions")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateDetectorModel = Action("UpdateDetectorModel")
UpdateInput = Action("UpdateInput")
UpdateInputRouting = Action("UpdateInputRouting")
