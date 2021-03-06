"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon Elastic Block Store"
prefix = "ebs"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CompleteSnapshot = Action("CompleteSnapshot")
GetSnapshotBlock = Action("GetSnapshotBlock")
ListChangedBlocks = Action("ListChangedBlocks")
ListSnapshotBlocks = Action("ListSnapshotBlocks")
PutSnapshotBlock = Action("PutSnapshotBlock")
StartSnapshot = Action("StartSnapshot")
