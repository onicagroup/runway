"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon Elastic Transcoder"
prefix = "elastictranscoder"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

CancelJob = Action("CancelJob")
CreateJob = Action("CreateJob")
CreatePipeline = Action("CreatePipeline")
CreatePreset = Action("CreatePreset")
DeletePipeline = Action("DeletePipeline")
DeletePreset = Action("DeletePreset")
ListJobsByPipeline = Action("ListJobsByPipeline")
ListJobsByStatus = Action("ListJobsByStatus")
ListPipelines = Action("ListPipelines")
ListPresets = Action("ListPresets")
ReadJob = Action("ReadJob")
ReadPipeline = Action("ReadPipeline")
ReadPreset = Action("ReadPreset")
TestRole = Action("TestRole")
UpdatePipeline = Action("UpdatePipeline")
UpdatePipelineNotifications = Action("UpdatePipelineNotifications")
UpdatePipelineStatus = Action("UpdatePipelineStatus")
