"""This type stub file was generated by pyright."""

from __future__ import annotations

from docker.models.resource import Collection, Model

class Plugin(Model):
    def __repr__(self): ...
    @property
    def name(self): ...
    @property
    def enabled(self): ...
    @property
    def settings(self): ...
    def configure(self, options): ...
    def disable(self): ...
    def enable(self, timeout=...): ...
    def push(self): ...
    def remove(self, force=...): ...
    def upgrade(self, remote=...): ...

class PluginCollection(Collection):
    model = Plugin
    def create(self, name, plugin_data_dir, gzip=...): ...
    def get(self, name): ...
    def install(self, remote_name, local_name=...): ...
    def list(self): ...
