"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "AWS Savings Plans"
prefix = "savingsplans"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateSavingsPlan = Action("CreateSavingsPlan")
DeleteQueuedSavingsPlan = Action("DeleteQueuedSavingsPlan")
DescribeSavingsPlanRates = Action("DescribeSavingsPlanRates")
DescribeSavingsPlans = Action("DescribeSavingsPlans")
DescribeSavingsPlansOfferingRates = Action("DescribeSavingsPlansOfferingRates")
DescribeSavingsPlansOfferings = Action("DescribeSavingsPlansOfferings")
ListTagsForResource = Action("ListTagsForResource")
TagResource = Action("TagResource")
UntagResource = Action("UntagResource")
