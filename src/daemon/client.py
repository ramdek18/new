import asyncio

import aiohttp

from src.proxy.client import request_response_proxy
from src.util.path import mkdir


def should_use_unix_socket():
    """
    Use unix sockets unless they are not supported. Check `socket` to see.
    """
    import socket
    return hasattr(socket, "AF_UNIX")


def socket_server_path(root_path):
    """
    This is the file that's either the unix socket or a text file containing
    the TCP socket information (ie. the port).
    """
    return root_path / "run" / "start-daemon.socket"


async def client_rw_for_start_daemon(root_path, use_unix_socket):
    """
    Connect to the unix or TCP socket, and return the reader & writer.
    """
    path = socket_server_path(root_path)
    mkdir(path.parent)
    try:
        if use_unix_socket:
            r, w = await asyncio.open_unix_connection(path)
        else:
            with open(path) as f:
                port = int(f.readline())
            r, w = await asyncio.open_connection("127.0.0.1", port=port)
        return r, w
    except Exception as ex:
        pass

    return None


class DaemonProxy:
    def __init__(self, host, port):
        self._prefix = f"http://{host}:{port}"

    async def _get(self, uri):
        url = f"{self._prefix}{uri}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                r = await response.text()
        return r

    async def start_service(self, service_name):
        uri = f"/daemon/service/start/?service={service_name}"
        return await self._get(uri)

    async def stop_service(self, service_name, delay_before_kill=15):
        uri = f"/daemon/service/stop/?service={service_name}"
        return await self._get(uri)

    async def is_running(self, service_name):
        uri = f"/daemon/service/is_running/?service={service_name}"
        return await self._get(uri)

    async def ping(self):
        uri = f"/daemon/ping/"
        return await self._get(uri)

    async def exit(self):
        uri = f"/daemon/exit/"
        return await self._get(uri)


async def connect_to_daemon(root_path, use_unix_socket):
    """
    Connect to the local daemon.
    """
    return DaemonProxy(host='127.0.0.1', port=8080)

    reader, writer = await client_rw_for_start_daemon(root_path, use_unix_socket)
    return request_response_proxy(reader, writer)


async def connect_to_daemon_and_validate(root_path):
    """
    Connect to the local daemon and do a ping to ensure that something is really
    there and running.
    """
    use_unix_socket = should_use_unix_socket()
    try:
        connection = await connect_to_daemon(root_path, use_unix_socket)
        r = await connection.ping()
        if r == "pong":
            return connection
    except Exception as ex:
        pass
    return None
