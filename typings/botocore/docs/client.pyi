"""
This type stub file was generated by pyright.
"""

class ClientDocumenter(object):
    def __init__(self, client, shared_examples=...) -> None: ...
    def document_client(self, section):
        """Documents a client and its methods

        :param section: The section to write to.
        """
        ...

class ClientExceptionsDocumenter(object):
    _USER_GUIDE_LINK = ...
    _GENERIC_ERROR_SHAPE = ...
    def __init__(self, client) -> None: ...
    def document_exceptions(self, section): ...
