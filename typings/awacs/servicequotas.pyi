"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Service Quotas"
prefix = "servicequotas"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

AssociateServiceQuotaTemplate = Action("AssociateServiceQuotaTemplate")
DeleteServiceQuotaIncreaseRequestFromTemplate = Action(
    "DeleteServiceQuotaIncreaseRequestFromTemplate"
)
DisassociateServiceQuotaTemplate = Action("DisassociateServiceQuotaTemplate")
GetAWSDefaultServiceQuota = Action("GetAWSDefaultServiceQuota")
GetAssociationForServiceQuotaTemplate = Action("GetAssociationForServiceQuotaTemplate")
GetRequestedServiceQuotaChange = Action("GetRequestedServiceQuotaChange")
GetServiceQuota = Action("GetServiceQuota")
GetServiceQuotaIncreaseRequestFromTemplate = Action("GetServiceQuotaIncreaseRequestFromTemplate")
ListAWSDefaultServiceQuotas = Action("ListAWSDefaultServiceQuotas")
ListRequestedServiceQuotaChangeHistory = Action("ListRequestedServiceQuotaChangeHistory")
ListRequestedServiceQuotaChangeHistoryByQuota = Action(
    "ListRequestedServiceQuotaChangeHistoryByQuota"
)
ListServiceQuotaIncreaseRequestsInTemplate = Action("ListServiceQuotaIncreaseRequestsInTemplate")
ListServiceQuotas = Action("ListServiceQuotas")
ListServices = Action("ListServices")
PutServiceQuotaIncreaseRequestIntoTemplate = Action("PutServiceQuotaIncreaseRequestIntoTemplate")
RequestServiceQuotaIncrease = Action("RequestServiceQuotaIncrease")
