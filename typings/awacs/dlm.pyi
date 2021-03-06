"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon Data Lifecycle Manager"
prefix = "dlm"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateLifecyclePolicy = Action("CreateLifecyclePolicy")
DeleteLifecyclePolicy = Action("DeleteLifecyclePolicy")
GetLifecyclePolicies = Action("GetLifecyclePolicies")
GetLifecyclePolicy = Action("GetLifecyclePolicy")
ListTagsForResource = Action("ListTagsForResource")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateLifecyclePolicy = Action("UpdateLifecyclePolicy")
