"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon Redshift Data API"
prefix = "redshift-data"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CancelStatement = Action("CancelStatement")
DescribeStatement = Action("DescribeStatement")
DescribeTable = Action("DescribeTable")
ExecuteStatement = Action("ExecuteStatement")
GetStatementResult = Action("GetStatementResult")
ListDatabases = Action("ListDatabases")
ListSchemas = Action("ListSchemas")
ListStatements = Action("ListStatements")
ListTables = Action("ListTables")
