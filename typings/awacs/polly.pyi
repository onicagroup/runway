"""
This type stub file was generated by pyright.
"""

from .aws import Action as BaseAction
from .aws import BaseARN

service_name = "Amazon Polly"
prefix = "polly"

class Action(BaseAction):
    def __init__(self, action=...) -> None: ...

class ARN(BaseARN):
    def __init__(self, resource=..., region=..., account=...) -> None: ...

DeleteLexicon = Action("DeleteLexicon")
DescribeVoices = Action("DescribeVoices")
GetLexicon = Action("GetLexicon")
GetSpeechSynthesisTask = Action("GetSpeechSynthesisTask")
ListLexicons = Action("ListLexicons")
ListSpeechSynthesisTasks = Action("ListSpeechSynthesisTasks")
PutLexicon = Action("PutLexicon")
StartSpeechSynthesisTask = Action("StartSpeechSynthesisTask")
SynthesizeSpeech = Action("SynthesizeSpeech")
