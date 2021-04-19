"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Accounts"
prefix = "account"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

DisableRegion = Action("DisableRegion")
EnableRegion = Action("EnableRegion")
ListRegions = Action("ListRegions")