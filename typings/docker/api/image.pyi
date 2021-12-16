"""This type stub file was generated by pyright."""
# pylint: disable=C,E,W,R
from __future__ import annotations

import logging
from typing import Any, Dict, Iterator, List, Optional, Union

from docker import utils

log: logging.Logger = ...

class ImageApiMixin:
    @utils.check_resource("image")
    def get_image(self, image: str, chunk_size: int = ...) -> Iterator[bytes]: ...
    @utils.check_resource("image")
    def history(self, image: str) -> str: ...
    def images(
        self,
        name: str = ...,
        quiet: bool = ...,
        all: bool = ...,
        filters: Optional[Dict[str, Any]] = ...,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]: ...
    def import_image(
        self, src=..., repository=..., tag=..., image=..., changes=..., stream_src=...
    ): ...
    def import_image_from_data(self, data, repository=..., tag=..., changes=...): ...
    def import_image_from_file(
        self, filename, repository=..., tag=..., changes=...
    ): ...
    def import_image_from_stream(
        self, stream, repository=..., tag=..., changes=...
    ): ...
    def import_image_from_url(self, url, repository=..., tag=..., changes=...): ...
    def import_image_from_image(self, image, repository=..., tag=..., changes=...): ...
    @utils.check_resource("image")
    def inspect_image(self, image: str) -> Dict[str, Any]: ...
    @utils.minimum_version("1.30")
    @utils.check_resource("image")
    def inspect_distribution(
        self, image: str, auth_config: Optional[Dict[str, Any]] = ...
    ) -> Dict[str, Any]: ...
    def load_image(
        self, data: bytes, quiet: bool = ...
    ) -> Iterator[Dict[str, Any]]: ...
    @utils.minimum_version("1.25")
    def prune_images(
        self, filters: Optional[Dict[str, Any]] = ...
    ) -> Dict[str, Any]: ...
    def pull(
        self,
        repository: Optional[str],
        tag: Optional[str] = ...,
        stream: bool = ...,
        auth_config: Optional[Dict[str, Any]] = ...,
        decode: bool = ...,
        platform: Optional[str] = ...,
        all_tags: bool = ...,
    ) -> Union[Iterator[Dict[str, Any]], Iterator[bytes], Iterator[str], str]: ...
    def push(
        self,
        repository: Optional[str],
        tag: Optional[str] = ...,
        stream: bool = ...,
        auth_config: Optional[Dict[str, Any]] = ...,
        decode: bool = ...,
    ) -> Union[Iterator[Dict[str, Any]], Iterator[bytes], Iterator[str], str]: ...
    @utils.check_resource("image")
    def remove_image(
        self, image: str, force: bool = ..., noprune: bool = ...
    ) -> Dict[str, Any]: ...
    def search(self, term: str, limit: Optional[int] = ...) -> List[Dict[str, Any]]: ...
    @utils.check_resource("image")
    def tag(
        self, image: str, repository: Optional[str], tag: str = ..., force: bool = ...
    ) -> bool: ...

def is_file(src: str) -> bool: ...