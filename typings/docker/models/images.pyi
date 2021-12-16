"""This type stub file was generated by pyright."""
# pylint: disable=C,E,W,R
from __future__ import annotations

from typing import Any, BinaryIO, Dict, Iterator, List, Optional, Tuple, Union, overload

from docker.models.resource import Collection, Model
from typing_extensions import Literal

class Image(Model):
    def __repr__(self) -> str: ...
    @property
    def labels(self) -> Dict[str, str]: ...
    @property
    def short_id(self) -> str: ...
    @property
    def tags(self) -> List[str]: ...
    def history(self) -> str: ...
    def save(
        self, chunk_size: int = ..., named: Union[bool, str] = ...
    ) -> Iterator[bytes]: ...
    def tag(
        self,
        repository: Optional[str],
        tag: str = ...,
        *,
        force: bool = ...,
        **kwargs: Any,
    ) -> bool: ...

class RegistryData(Model):
    def __init__(self, image_name: str, *args: Any, **kwargs: Any) -> None: ...
    @property
    def id(self) -> str: ...
    @property
    def short_id(self) -> str: ...
    def pull(self, platform: Optional[str] = ...) -> Image: ...
    def has_platform(self, platform: Union[str, Dict[str, Any]]) -> bool: ...
    def reload(self) -> None: ...

class ImageCollection(Collection):
    model = Image
    def build(
        self,
        *,
        buildargs: Optional[Dict[str, Any]] = ...,
        cache_from: Optional[List[str]] = ...,
        container_limits: Optional[Dict[str, Any]] = ...,
        custom_context: bool = ...,
        dockerfile: Optional[str] = ...,
        encoding: Optional[str] = ...,
        extra_hosts: Optional[Dict[str, Any]] = ...,
        fileobj: Optional[BinaryIO] = ...,
        forcerm: bool = ...,
        isolation: Optional[str] = ...,
        labels: Optional[Dict[str, str]] = ...,
        network_mode: Optional[str] = ...,
        nocache: bool = ...,
        path: Optional[str] = ...,
        platform: Optional[str] = ...,
        pull: bool = ...,
        quiet: bool = ...,
        rm: bool = ...,
        shmsize: Optional[int] = ...,
        squash: bool = ...,
        tag: Optional[str] = ...,
        target: Optional[str] = ...,
        timeout: Optional[int] = ...,
        use_config_proxy: bool = ...,
    ) -> Tuple[Image, Iterator[Dict[str, str]]]: ...
    def get(self, name: str) -> Image: ...
    def get_registry_data(
        self, name: str, auth_config: Dict[str, Any] = ...
    ) -> RegistryData: ...
    def list(
        self,
        name: Optional[str] = ...,
        all: bool = ...,
        filters: Optional[Dict[str, Any]] = ...,
    ) -> List[Image]: ...
    def load(self, data: bytes) -> List[Image]: ...
    @overload
    def pull(
        self,
        repository: Optional[str],
        tag: Optional[str] = ...,
        all_tags: Literal[False] = ...,
        *,
        auth_config: Optional[Dict[str, Any]] = ...,
        platform: Optional[str] = ...,
    ) -> Image: ...
    @overload
    def pull(
        self,
        repository: Optional[str],
        tag: Optional[str] = ...,
        all_tags: Literal[True] = ...,
        *,
        auth_config: Optional[Dict[str, Any]] = ...,
        platform: Optional[str] = ...,
    ) -> List[Image]: ...
    def pull(
        self,
        repository: Optional[str],
        tag: Optional[str] = ...,
        all_tags: bool = ...,
        *,
        auth_config: Optional[Dict[str, Any]] = ...,
        platform: Optional[str] = ...,
    ) -> Union[List[Image], Image]: ...
    @overload
    def push(
        self,
        repository: Optional[str],
        tag: Optional[str] = ...,
        *,
        auth_config: Optional[Dict[str, Any]] = ...,
        decode: bool = ...,
        stream: Literal[False] = ...,
    ) -> str: ...
    @overload
    def push(
        self,
        repository: Optional[str],
        tag: Optional[str] = ...,
        *,
        auth_config: Optional[Dict[str, Any]] = ...,
        decode: bool = ...,
        stream: Literal[True] = ...,
    ) -> Iterator[str]: ...
    def push(
        self,
        repository: Optional[str],
        tag: Optional[str] = ...,
        *,
        auth_config: Optional[Dict[str, Any]] = ...,
        decode: bool,
        stream: bool = ...,
    ) -> Union[Iterator[str], str]: ...
    def remove(
        self, *args: Any, force: bool = ..., image: str, noprune: bool = ...
    ) -> Any: ...
    def search(
        self, *args: Any, limit: Optional[int] = ..., term: str
    ) -> List[Dict[str, Any]]: ...
    def prune(self, filters: Optional[Dict[str, Any]] = ...) -> Dict[str, Any]: ...
    def prune_builds(self, *args: Any, **kwargs: Any) -> Dict[str, Any]: ...

def normalize_platform(
    platform: Optional[Dict[str, Any]], engine_info: Dict[str, Any]
) -> Dict[str, Any]: ...