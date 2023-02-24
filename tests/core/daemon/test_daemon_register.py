from __future__ import annotations

from typing import Any

import aiohttp
import pytest

from chia.util.ws_message import create_payload


@pytest.mark.asyncio
async def test_multiple_register_same(get_daemon: Any, bt: Any) -> None:
    ws_server = get_daemon
    config = bt.config

    daemon_port = config["daemon_port"]

    # setup receive service to connect to the daemon
    client = aiohttp.ClientSession()
    ws = await client.ws_connect(
        f"wss://127.0.0.1:{daemon_port}",
        autoclose=True,
        autoping=True,
        ssl_context=bt.get_daemon_ssl_context(),
        max_msg_size=100 * 1024 * 1024,
    )

    service_name = "test_service"
    data = {"service": service_name}
    payload = create_payload("register_service", data, service_name, "daemon")
    await ws.send_str(payload)
    await ws.receive()
    payload = create_payload("register_service", data, service_name, "daemon")
    await ws.send_str(payload)
    await ws.receive()
    payload = create_payload("register_service", data, service_name, "daemon")
    await ws.send_str(payload)
    await ws.receive()
    payload = create_payload("register_service", data, service_name, "daemon")
    await ws.send_str(payload)
    await ws.receive()

    connections = ws_server.connections.get(service_name, {})
    assert len(connections) == 1

    await client.close()
    await ws_server.stop()


@pytest.mark.asyncio
async def test_multiple_register_different(get_daemon: Any, bt: Any) -> None:
    ws_server = get_daemon
    config = bt.config

    daemon_port = config["daemon_port"]

    # setup receive service to connect to the daemon
    client = aiohttp.ClientSession()
    ws = await client.ws_connect(
        f"wss://127.0.0.1:{daemon_port}",
        autoclose=True,
        autoping=True,
        ssl_context=bt.get_daemon_ssl_context(),
        max_msg_size=100 * 1024 * 1024,
    )

    test_service_names = ["service1, service2", "service3"]

    for service_name in test_service_names:
        data = {"service": service_name}
        payload = create_payload("register_service", data, service_name, "daemon")
        await ws.send_str(payload)
        await ws.receive()

    for service_name in test_service_names:
        connections = ws_server.connections.get(service_name, {})
        assert len(connections) == 1

    await ws.close()

    for service_name in test_service_names:
        connections = ws_server.connections.get(service_name, {})
        assert len(connections) == 0

    await client.close()
    await ws_server.stop()


@pytest.mark.asyncio
async def test_remove_connection(get_daemon: Any, bt: Any) -> None:
    ws_server = get_daemon
    config = bt.config

    daemon_port = config["daemon_port"]

    # setup receive service to connect to the daemon
    client = aiohttp.ClientSession()
    ws = await client.ws_connect(
        f"wss://127.0.0.1:{daemon_port}",
        autoclose=True,
        autoping=True,
        ssl_context=bt.get_daemon_ssl_context(),
        max_msg_size=100 * 1024 * 1024,
    )

    test_service_names = ["service1, service2, service3, service4, service5"]

    for service_name in test_service_names:
        data = {"service": service_name}
        payload = create_payload("register_service", data, service_name, "daemon")
        await ws.send_str(payload)
        await ws.receive()

    ws_response_set = ws_server.connections.get(test_service_names[0], {})
    assert len(ws_response_set) == 1

    removed_names = ws_server.remove_connection(min(ws_response_set))

    assert removed_names == test_service_names

    await client.close()
    await ws_server.stop()
