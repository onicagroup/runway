"""This type stub file was generated by pyright."""
# pylint: disable=C,E,W,R
from __future__ import annotations

from typing import Optional

import requests

class DockerException(Exception): ...

def create_api_error_from_http_exception(
    e: requests.exceptions.HTTPError,
) -> APIError: ...

class APIError(requests.exceptions.HTTPError, DockerException):
    explanation: Optional[str]
    response: Optional[requests.Response]
    def __init__(
        self,
        message: str,
        response: Optional[requests.Response] = ...,
        explanation: Optional[str] = ...,
    ) -> None: ...
    def __str__(self) -> str: ...
    @property
    def status_code(self) -> Optional[int]: ...
    def is_error(self) -> bool: ...
    def is_client_error(self) -> bool: ...
    def is_server_error(self) -> bool: ...

class NotFound(APIError): ...
class ImageNotFound(NotFound): ...
class InvalidVersion(DockerException): ...
class InvalidRepository(DockerException): ...
class InvalidConfigFile(DockerException): ...
class InvalidArgument(DockerException): ...
class DeprecatedMethod(DockerException): ...

class TLSParameterError(DockerException):
    def __init__(self, msg) -> None: ...
    def __str__(self) -> str: ...

class NullResource(DockerException, ValueError): ...

class ContainerError(DockerException):
    def __init__(self, container, exit_status, command, image, stderr) -> None: ...

class StreamParseError(RuntimeError):
    def __init__(self, reason) -> None: ...

class BuildError(DockerException):
    def __init__(self, reason, build_log) -> None: ...

class ImageLoadError(DockerException): ...

def create_unexpected_kwargs_error(name, kwargs): ...

class MissingContextParameter(DockerException):
    def __init__(self, param) -> None: ...
    def __str__(self) -> str: ...

class ContextAlreadyExists(DockerException):
    def __init__(self, name) -> None: ...
    def __str__(self) -> str: ...

class ContextException(DockerException):
    def __init__(self, msg) -> None: ...
    def __str__(self) -> str: ...

class ContextNotFound(DockerException):
    def __init__(self, name) -> None: ...
    def __str__(self) -> str: ...
