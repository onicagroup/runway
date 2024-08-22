"""This type stub file was generated by pyright."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Generic, Optional, TextIO, TypeVar

from .futures import BaseExecutor, TransferFuture
from .subscribers import BaseSubscriber
from .utils import OSUtils

if TYPE_CHECKING:
    from logging import Logger
    from re import Pattern

    from mypy_boto3_s3 import S3Client

logger: Logger = ...

class TransferConfig:
    io_chunksize: int
    max_bandwidth: Optional[int]
    max_in_memory_download_chunks: int
    max_in_memory_upload_chunks: int
    max_io_queue_size: int
    max_request_concurrency: int
    max_request_queue_size: int
    max_submission_concurrency: int
    max_submission_queue_size: int
    multipart_chunksize: int
    multipart_threshold: int
    num_download_attempts: int
    def __init__(
        self,
        multipart_threshold: int = ...,
        multipart_chunksize: int = ...,
        max_request_concurrency: int = ...,
        max_submission_concurrency: int = ...,
        max_request_queue_size: int = ...,
        max_submission_queue_size: int = ...,
        max_io_queue_size: int = ...,
        io_chunksize: int = ...,
        num_download_attempts: int = ...,
        max_in_memory_upload_chunks: int = ...,
        max_in_memory_download_chunks: int = ...,
        max_bandwidth: Optional[int] = ...,
    ) -> None: ...

class TransferManager:
    ALLOWED_DOWNLOAD_ARGS: ClassVar[list[str]] = ...
    ALLOWED_UPLOAD_ARGS: ClassVar[list[str]] = ...
    ALLOWED_COPY_ARGS: ClassVar[list[str]] = ...
    ALLOWED_DELETE_ARGS: ClassVar[list[str]] = ...
    VALIDATE_SUPPORTED_BUCKET_VALUES: ClassVar[bool] = ...
    _UNSUPPORTED_BUCKET_PATTERNS: ClassVar[dict[str, Pattern[str]]] = ...
    def __init__(
        self,
        client: S3Client,
        config: Optional[TransferConfig] = ...,
        osutil: Optional[OSUtils] = ...,
        executor_cls: Optional[type[BaseExecutor]] = ...,
    ) -> None: ...
    @property
    def client(self) -> S3Client: ...
    @property
    def config(self) -> TransferConfig: ...
    def upload(
        self,
        fileobj: str | TextIO,
        bucket: str,
        key: str,
        extra_args: Optional[dict[str, Any]] = ...,
        subscribers: Optional[list[BaseSubscriber]] = ...,
    ) -> TransferFuture: ...
    def download(
        self,
        bucket: str,
        key: str,
        fileobj: str | TextIO,
        extra_args: Optional[dict[str, Any]] = ...,
        subscribers: Optional[list[BaseSubscriber]] = ...,
    ) -> TransferFuture: ...
    def copy(
        self,
        copy_source: dict[str, str],
        bucket: str,
        key: str,
        extra_args: Optional[dict[str, Any]] = ...,
        subscribers: Optional[list[BaseSubscriber]] = ...,
        source_client: S3Client = ...,
    ) -> TransferFuture: ...
    def delete(
        self,
        bucket: str,
        key: str,
        extra_args: Optional[dict[str, Any]] = ...,
        subscribers: Optional[list[BaseSubscriber]] = ...,
    ) -> TransferFuture: ...
    def __enter__(self) -> TransferConfig: ...
    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        *args: Any,
    ) -> None: ...
    def shutdown(self, cancel: bool = ..., cancel_msg: str = ...) -> None: ...

_T = TypeVar("_T")

class TransferCoordinatorController(Generic[_T]):
    def __init__(self) -> None: ...
    @property
    def tracked_transfer_coordinators(self) -> set[_T]: ...
    def add_transfer_coordinator(self, transfer_coordinator: _T) -> None: ...
    def remove_transfer_coordinator(self, transfer_coordinator: _T) -> None: ...
    def cancel(self, msg: str = ..., exc_type: type[BaseException] = ...) -> None: ...
    def wait(self) -> None: ...
