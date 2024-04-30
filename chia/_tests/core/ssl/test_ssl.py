from __future__ import annotations

import asyncio
import contextlib
import ssl

import aiohttp
import pytest
import logging
from chia.protocols.shared_protocol import capabilities
from chia.server.outbound_message import NodeType
from chia.server.server import ChiaServer, ssl_context_for_client
from chia.server.ssl_context import chia_ssl_ca_paths, private_ssl_ca_paths
from chia.server.ws_connection import WSChiaConnection
from chia.ssl.create_ssl import generate_ca_signed_cert
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.peer_info import PeerInfo


async def establish_connection(server: ChiaServer, self_hostname: str, ssl_context) -> None:
    timeout = aiohttp.ClientTimeout(total=10)
    dummy_port = 5  # this does not matter
    async with aiohttp.ClientSession(timeout=timeout) as session:
        url = f"wss://{self_hostname}:{server._port}/ws"
        ws = await session.ws_connect(url, autoclose=False, autoping=True, ssl=ssl_context)
        wsc = WSChiaConnection.create(
            NodeType.FULL_NODE,
            ws,
            server.api,
            dummy_port,
            server.log,
            True,
            server.received_message_callback,
            None,
            bytes32(b"\x00" * 32),
            100,
            30,
            local_capabilities_for_handshake=capabilities,
        )
        await wsc.perform_handshake(server._network_id, dummy_port, NodeType.FULL_NODE)
        await wsc.close()


ssl_cert_error = False


class TestSSL:
    @pytest.mark.anyio
    async def test_public_connections(self, simulator_and_wallet, self_hostname):
        full_nodes, wallets, _ = simulator_and_wallet
        full_node_api = full_nodes[0]
        server_1: ChiaServer = full_node_api.full_node.server
        wallet_node, server_2 = wallets[0]

        success = await server_2.start_client(PeerInfo(self_hostname, server_1.get_port()), None)
        assert success is True

    @pytest.mark.anyio
    async def test_farmer(self, farmer_one_harvester_not_started, self_hostname, caplog):

        _, farmer_service, bt = farmer_one_harvester_not_started
        farmer_api = farmer_service._api

        farmer_server = farmer_api.farmer.server
        ca_private_crt_path, ca_private_key_path = private_ssl_ca_paths(bt.root_path, bt.config)
        chia_ca_crt_path, chia_ca_key_path = chia_ssl_ca_paths(bt.root_path, bt.config)
        # Create valid cert (valid meaning signed with private CA)
        priv_crt = farmer_server.root_path / "valid.crt"
        priv_key = farmer_server.root_path / "valid.key"
        generate_ca_signed_cert(
            ca_private_crt_path.read_bytes(),
            ca_private_key_path.read_bytes(),
            priv_crt,
            priv_key,
        )

        async with farmer_service.manage():
            # ssl_context = ssl_context_for_client(ca_private_crt_path, ca_private_key_path, priv_crt, priv_key)
            # await establish_connection(farmer_server, self_hostname, ssl_context)

            # Create not authenticated cert
            pub_crt = farmer_server.root_path / "non_valid.crt"
            pub_key = farmer_server.root_path / "non_valid.key"
            generate_ca_signed_cert(chia_ca_crt_path.read_bytes(), chia_ca_key_path.read_bytes(), pub_crt, pub_key)
            # ssl_context = ssl_context_for_client(chia_ca_crt_path, chia_ca_key_path, pub_crt, pub_key)
            # with pytest.raises(aiohttp.ClientConnectorCertificateError):
            #    await establish_connection(farmer_server, self_hostname, ssl_context)
            ssl_context = ssl_context_for_client(ca_private_crt_path, ca_private_key_path, pub_crt, pub_key)
            try:
                asyncio.get_event_loop().set_debug(True)
                with caplog.at_level(logging.DEBUG, logger="asyncio"):
                    await establish_connection(farmer_server, self_hostname, ssl_context)
            except Exception:
                pass  # ignore any exceptions and just check the expected log output below
            finally:
                assert "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate signature failure" in caplog.text
                asyncio.get_event_loop().set_debug(False)


    @pytest.mark.anyio
    async def test_full_node(self, simulator_and_wallet, self_hostname):
        full_nodes, wallets, bt = simulator_and_wallet
        full_node_api = full_nodes[0]
        full_node_server = full_node_api.full_node.server
        chia_ca_crt_path, chia_ca_key_path = chia_ssl_ca_paths(bt.root_path, bt.config)

        # Create not authenticated cert
        pub_crt = full_node_server.root_path / "p2p.crt"
        pub_key = full_node_server.root_path / "p2p.key"
        generate_ca_signed_cert(
            chia_ca_crt_path.read_bytes(),
            chia_ca_key_path.read_bytes(),
            pub_crt,
            pub_key,
        )
        ssl_context = ssl_context_for_client(chia_ca_crt_path, chia_ca_key_path, pub_crt, pub_key)
        await establish_connection(full_node_server, self_hostname, ssl_context)

    @pytest.mark.anyio
    async def test_introducer(self, introducer_service, self_hostname):
        introducer_server = introducer_service._node.server
        chia_ca_crt_path, chia_ca_key_path = chia_ssl_ca_paths(introducer_service.root_path, introducer_service.config)

        # Create not authenticated cert
        pub_crt = introducer_server.root_path / "p2p.crt"
        pub_key = introducer_server.root_path / "p2p.key"
        generate_ca_signed_cert(
            chia_ca_crt_path.read_bytes(),
            chia_ca_key_path.read_bytes(),
            pub_crt,
            pub_key,
        )
        ssl_context = ssl_context_for_client(chia_ca_crt_path, chia_ca_key_path, pub_crt, pub_key)
        await establish_connection(introducer_server, self_hostname, ssl_context)
