"""This type stub file was generated by pyright."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .tasks import SubmissionTask, Task

if TYPE_CHECKING:
    from logging import Logger

logger: Logger = ...

class DownloadOutputManager:
    def __init__(self, osutil, transfer_coordinator, io_executor) -> None: ...
    @classmethod
    def is_compatible(cls, download_target, osutil): ...
    def get_download_task_tag(self): ...
    def get_fileobj_for_io_writes(self, transfer_future): ...
    def queue_file_io_task(self, fileobj, data, offset): ...
    def get_io_write_task(self, fileobj, data, offset): ...
    def get_final_io_task(self): ...

class DownloadFilenameOutputManager(DownloadOutputManager):
    def __init__(self, osutil, transfer_coordinator, io_executor) -> None: ...
    @classmethod
    def is_compatible(cls, download_target, osutil): ...
    def get_fileobj_for_io_writes(self, transfer_future): ...
    def get_final_io_task(self): ...

class DownloadSeekableOutputManager(DownloadOutputManager):
    @classmethod
    def is_compatible(cls, download_target, osutil): ...
    def get_fileobj_for_io_writes(self, transfer_future): ...
    def get_final_io_task(self): ...

class DownloadNonSeekableOutputManager(DownloadOutputManager):
    def __init__(self, osutil, transfer_coordinator, io_executor, defer_queue=...) -> None: ...
    @classmethod
    def is_compatible(cls, download_target, osutil): ...
    def get_download_task_tag(self): ...
    def get_fileobj_for_io_writes(self, transfer_future): ...
    def get_final_io_task(self): ...
    def queue_file_io_task(self, fileobj, data, offset): ...
    def get_io_write_task(self, fileobj, data, offset): ...

class DownloadSpecialFilenameOutputManager(DownloadNonSeekableOutputManager):
    def __init__(self, osutil, transfer_coordinator, io_executor, defer_queue=...) -> None: ...
    @classmethod
    def is_compatible(cls, download_target, osutil): ...
    def get_fileobj_for_io_writes(self, transfer_future): ...
    def get_final_io_task(self): ...

class DownloadSubmissionTask(SubmissionTask): ...
class GetObjectTask(Task): ...
class ImmediatelyWriteIOGetObjectTask(GetObjectTask): ...
class IOWriteTask(Task): ...
class IOStreamingWriteTask(Task): ...
class IORenameFileTask(Task): ...
class IOCloseTask(Task): ...

class CompleteDownloadNOOPTask(Task):
    def __init__(
        self,
        transfer_coordinator,
        main_kwargs=...,
        pending_main_kwargs=...,
        done_callbacks=...,
        is_final=...,
    ) -> None: ...

class DownloadChunkIterator:
    def __init__(self, body, chunksize) -> None: ...
    def __iter__(self): ...
    def __next__(self): ...
    next = ...

class DeferQueue:
    def __init__(self) -> None: ...
    def request_writes(self, offset, data): ...
