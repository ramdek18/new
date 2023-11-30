from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Tuple, cast

from chia.full_node.full_node import FullNode
from chia.rpc.full_node_rpc_api import FullNodeRpcApi
from chia.rpc.rpc_server import RpcServer
from chia.server.server import ChiaServer
from chia.server.start_service import Service
from chia.simulator.full_node_simulator import FullNodeSimulator
from tests.environments.common import ServiceEnvironment


@dataclass
class FullNodeEnvironment:
    if TYPE_CHECKING:
        _protocol_check: ClassVar[ServiceEnvironment[FullNode, FullNodeRpcApi, FullNodeSimulator]] = cast(
            "FullNodeEnvironment",
            None,
        )

    __match_args__: ClassVar[Tuple[str, ...]] = ()

    service: Service[FullNode, FullNodeSimulator]

    @property
    def node(self) -> FullNode:
        return self.service._node

    @property
    def rpc_api(self) -> FullNodeRpcApi:
        assert self.service.rpc_server is not None
        # TODO: hinting...?
        return self.service.rpc_server.rpc_api  # type: ignore[return-value]

    @property
    def rpc_server(self) -> RpcServer:
        assert self.service.rpc_server is not None
        return self.service.rpc_server

    @property
    def peer_api(self) -> FullNodeSimulator:
        return self.service._api

    @property
    def peer_server(self) -> ChiaServer:
        return self.service._server
