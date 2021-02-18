"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Elemental Appliances and Software"
prefix = "elemental-appliances-software"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateQuote = Action("CreateQuote")
GetQuote = Action("GetQuote")
ListQuotes = Action("ListQuotes")
ListTagsForResource = Action("ListTagsForResource")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
UpdateQuote = Action("UpdateQuote")
