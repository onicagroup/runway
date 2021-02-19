"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon RDS Data API"
prefix = "rds-data"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

BatchExecuteStatement = Action("BatchExecuteStatement")
BeginTransaction = Action("BeginTransaction")
CommitTransaction = Action("CommitTransaction")
ExecuteSql = Action("ExecuteSql")
ExecuteStatement = Action("ExecuteStatement")
RollbackTransaction = Action("RollbackTransaction")
