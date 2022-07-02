import logging
import pathlib
from typing import Dict

from chia.consensus.constants import ConsensusConstants
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.rpc.timelord_rpc_api import TimelordRpcApi
from chia.server.outbound_message import NodeType
from chia.server.start_service import run_service
from chia.timelord.timelord import Timelord
from chia.timelord.timelord_api import TimelordAPI
from chia.types.peer_info import PeerInfo
from chia.util.config import load_config, load_config_cli
from chia.util.default_root import DEFAULT_ROOT_PATH

# See: https://bugs.python.org/issue29288
"".encode("idna")

SERVICE_NAME = "timelord"


log = logging.getLogger(__name__)


def service_kwargs_for_timelord(
    root_path: pathlib.Path,
    full_config: Dict,
    constants: ConsensusConstants,
) -> Dict:
    service_config = full_config[SERVICE_NAME]

    connect_peers = [PeerInfo(service_config["full_node_peer"]["host"], service_config["full_node_peer"]["port"])]
    overrides = service_config["network_overrides"]["constants"][service_config["selected_network"]]
    updated_constants = constants.replace_str_to_bytes(**overrides)

    node = Timelord(root_path, service_config, updated_constants)
    peer_api = TimelordAPI(node)
    network_id = service_config["selected_network"]
    kwargs = dict(
        root_path=root_path,
        config=full_config,
        peer_api=peer_api,
        node=node,
        node_type=NodeType.TIMELORD,
        advertised_port=service_config["port"],
        service_name=SERVICE_NAME,
        server_listen_ports=[service_config["port"]],
        connect_peers=connect_peers,
        auth_connect_peers=False,
        network_id=network_id,
    )

    if service_config.get("start_rpc_server", True):
        kwargs["rpc_info"] = (TimelordRpcApi, service_config.get("rpc_port", 8557))

    return kwargs


def main() -> None:
    # TODO: refactor to avoid the double load
    full_config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    service_config = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", SERVICE_NAME)
    full_config[SERVICE_NAME] = service_config
    kwargs = service_kwargs_for_timelord(DEFAULT_ROOT_PATH, full_config, DEFAULT_CONSTANTS)
    return run_service(**kwargs)


if __name__ == "__main__":
    main()
