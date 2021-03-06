"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon FreeRTOS"
prefix = "freertos"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CreateSoftwareConfiguration = Action("CreateSoftwareConfiguration")
DeleteSoftwareConfiguration = Action("DeleteSoftwareConfiguration")
DescribeHardwarePlatform = Action("DescribeHardwarePlatform")
DescribeSoftwareConfiguration = Action("DescribeSoftwareConfiguration")
GetSoftwareURL = Action("GetSoftwareURL")
GetSoftwareURLForConfiguration = Action("GetSoftwareURLForConfiguration")
ListFreeRTOSVersions = Action("ListFreeRTOSVersions")
ListHardwarePlatforms = Action("ListHardwarePlatforms")
ListHardwareVendors = Action("ListHardwareVendors")
ListSoftwareConfigurations = Action("ListSoftwareConfigurations")
UpdateSoftwareConfiguration = Action("UpdateSoftwareConfiguration")
