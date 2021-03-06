"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Timestream"
prefix = "timestream"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CancelQuery = Action("CancelQuery")
CreateDatabase = Action("CreateDatabase")
CreateTable = Action("CreateTable")
DeleteDatabase = Action("DeleteDatabase")
DeleteTable = Action("DeleteTable")
DescribeDatabase = Action("DescribeDatabase")
DescribeEndpoints = Action("DescribeEndpoints")
DescribeTable = Action("DescribeTable")
ListDatabases = Action("ListDatabases")
ListMeasures = Action("ListMeasures")
ListTables = Action("ListTables")
ListTagsForResource = Action("ListTagsForResource")
Select = Action("Select")
SelectValues = Action("SelectValues")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateDatabase = Action("UpdateDatabase")
UpdateTable = Action("UpdateTable")
WriteRecords = Action("WriteRecords")
