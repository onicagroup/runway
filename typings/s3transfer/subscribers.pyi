"""This type stub file was generated by pyright."""

class BaseSubscriber:
    VALID_SUBSCRIBER_TYPES = ...
    def __new__(cls, *args, **kwargs): ...
    def on_queued(self, future, **kwargs): ...
    def on_progress(self, future, bytes_transferred, **kwargs): ...
    def on_done(self, future, **kwargs): ...
