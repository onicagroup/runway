"""
This type stub file was generated by pyright.
"""

import logging

HISTORY_RECORDER = None
logger = logging.getLogger(__name__)

class BaseHistoryHandler(object):
    def emit(self, event_type, payload, source): ...

class HistoryRecorder(object):
    def __init__(self) -> None: ...
    def enable(self): ...
    def disable(self): ...
    def add_handler(self, handler): ...
    def record(self, event_type, payload, source=...): ...

def get_global_history_recorder(): ...
