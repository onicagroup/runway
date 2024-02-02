"""This type stub file was generated by pyright."""

# pylint: disable=C,E,W,R
from __future__ import annotations

import sys

import urllib3
from docker.transport.basehttpadapter import BaseHTTPAdapter

PoolManager = urllib3.poolmanager.PoolManager
if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    ...

class SSLHTTPAdapter(BaseHTTPAdapter):
    __attrs__ = ...
    def __init__(
        self, ssl_version=..., assert_hostname=..., assert_fingerprint=..., **kwargs
    ) -> None: ...
    def init_poolmanager(self, connections, maxsize, block=...): ...
    def get_connection(self, *args, **kwargs): ...
    def can_override_ssl_version(self): ...
