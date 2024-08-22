"""This type stub file was generated by pyright."""

from __future__ import annotations

class SwarmSpec(dict):
    def __init__(
        self,
        version,
        task_history_retention_limit=...,
        snapshot_interval=...,
        keep_old_snapshots=...,
        log_entries_for_slow_followers=...,
        heartbeat_tick=...,
        election_tick=...,
        dispatcher_heartbeat_period=...,
        node_cert_expiry=...,
        external_cas=...,
        name=...,
        labels=...,
        signing_ca_cert=...,
        signing_ca_key=...,
        ca_force_rotate=...,
        autolock_managers=...,
        log_driver=...,
    ) -> None: ...

class SwarmExternalCA(dict):
    def __init__(self, url, protocol=..., options=..., ca_cert=...) -> None: ...
