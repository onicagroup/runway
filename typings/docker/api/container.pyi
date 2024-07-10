"""This type stub file was generated by pyright."""

from __future__ import annotations

from docker import utils

class ContainerApiMixin:
    @utils.check_resource("container")
    def attach(self, container, stdout=..., stderr=..., stream=..., logs=..., demux=...): ...
    @utils.check_resource("container")
    def attach_socket(self, container, params=..., ws=...): ...
    @utils.check_resource("container")
    def commit(
        self,
        container,
        repository=...,
        tag=...,
        message=...,
        author=...,
        changes=...,
        conf=...,
    ): ...
    def containers(
        self,
        quiet=...,
        all=...,
        trunc=...,
        latest=...,
        since=...,
        before=...,
        limit=...,
        size=...,
        filters=...,
    ): ...
    def create_container(
        self,
        image,
        command=...,
        hostname=...,
        user=...,
        detach=...,
        stdin_open=...,
        tty=...,
        ports=...,
        environment=...,
        volumes=...,
        network_disabled=...,
        name=...,
        entrypoint=...,
        working_dir=...,
        domainname=...,
        host_config=...,
        mac_address=...,
        labels=...,
        stop_signal=...,
        networking_config=...,
        healthcheck=...,
        stop_timeout=...,
        runtime=...,
        use_config_proxy=...,
    ): ...
    def create_container_config(self, *args, **kwargs): ...
    def create_container_from_config(self, config, name=...): ...
    def create_host_config(self, *args, **kwargs): ...
    def create_networking_config(self, *args, **kwargs): ...
    def create_endpoint_config(self, *args, **kwargs): ...
    @utils.check_resource("container")
    def diff(self, container): ...
    @utils.check_resource("container")
    def export(self, container, chunk_size=...): ...
    @utils.check_resource("container")
    def get_archive(self, container, path, chunk_size=..., encode_stream=...): ...
    @utils.check_resource("container")
    def inspect_container(self, container): ...
    @utils.check_resource("container")
    def kill(self, container, signal=...): ...
    @utils.check_resource("container")
    def logs(
        self,
        container,
        stdout=...,
        stderr=...,
        stream=...,
        timestamps=...,
        tail=...,
        since=...,
        follow=...,
        until=...,
    ): ...
    @utils.check_resource("container")
    def pause(self, container): ...
    @utils.check_resource("container")
    def port(self, container, private_port): ...
    @utils.check_resource("container")
    def put_archive(self, container, path, data): ...
    @utils.minimum_version("1.25")
    def prune_containers(self, filters=...): ...
    @utils.check_resource("container")
    def remove_container(self, container, v=..., link=..., force=...): ...
    @utils.check_resource("container")
    def rename(self, container, name): ...
    @utils.check_resource("container")
    def resize(self, container, height, width): ...
    @utils.check_resource("container")
    def restart(self, container, timeout=...): ...
    @utils.check_resource("container")
    def start(self, container, *args, **kwargs): ...
    @utils.check_resource("container")
    def stats(self, container, decode=..., stream=...): ...
    @utils.check_resource("container")
    def stop(self, container, timeout=...): ...
    @utils.check_resource("container")
    def top(self, container, ps_args=...): ...
    @utils.check_resource("container")
    def unpause(self, container): ...
    @utils.minimum_version("1.22")
    @utils.check_resource("container")
    def update_container(
        self,
        container,
        blkio_weight=...,
        cpu_period=...,
        cpu_quota=...,
        cpu_shares=...,
        cpuset_cpus=...,
        cpuset_mems=...,
        mem_limit=...,
        mem_reservation=...,
        memswap_limit=...,
        kernel_memory=...,
        restart_policy=...,
    ): ...
    @utils.check_resource("container")
    def wait(self, container, timeout=..., condition=...): ...
