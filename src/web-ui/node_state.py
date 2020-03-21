from aiohttp import client_exceptions
from src.rpc.rpc_client import RpcClient
from src.server.outbound_message import NodeType
from src.util.ints import uint64
from typing import List, Optional, Dict
from src.types.header_block import SmallHeaderBlock
import datetime


async def query_node(app):
    node = {}

    try:
        rpc_client: RpcClient = await RpcClient.create(app['config']['rpc_port'])

        connections = await rpc_client.get_connections()
        for con in connections:
            con['type_name'] = NodeType(con['type']).name

        blockchain_state = await rpc_client.get_blockchain_state()
        pool_balances = await rpc_client.get_pool_balances()

        coin_balances: Dict[
            bytes, uint64
        ] = pool_balances

        top_winners = sorted(
            [(rewards, key, bytes(key).hex()) for key, rewards in coin_balances.items()],
            reverse=True,
        )[: 10]

        our_winners = [
            (coin_balances[bytes(pk)], bytes(pk), bytes(pk).hex())
            if bytes(pk) in coin_balances
            else (0, bytes(pk), bytes(pk).hex())
            for pk in app['key_config']['pool_pks']
        ]

        latest_blocks = await get_latest_blocks(rpc_client, blockchain_state["tips"])

        rpc_client.close()

        node['connections'] = connections
        node['blockchain_state'] = blockchain_state
        node['pool_balances'] = pool_balances
        node['top_winners'] = top_winners
        node['our_winners'] = our_winners
        node['latest_blocks'] = latest_blocks
        node['state'] = 'Running'
        node['last_refresh'] = datetime.datetime.now()
        app['ready'] = True

    except client_exceptions.ClientConnectorError:
        node['state'] = 'Not running'

    finally:
        app['node'] = node


def find_block(block_list, blockid):
    for block in block_list:
        hash = str(block.challenge.proof_of_space_hash)
        if hash == blockid:
            return block

    return {}


def find_connection(connection_list, connectionid):
    for connection in connection_list:
        hash = str(connection['node_id'])
        if hash == connectionid:
            return connection

    return {}


async def get_latest_blocks(rpc_client: RpcClient, heads: List[SmallHeaderBlock]) -> List[SmallHeaderBlock]:
    added_blocks: List[SmallHeaderBlock] = []
    num_blocks = 10
    while len(added_blocks) < num_blocks and len(heads) > 0:
        heads = sorted(heads, key=lambda b: b.height, reverse=True)
        max_block = heads[0]
        if max_block not in added_blocks:
            added_blocks.append(max_block)
        heads.remove(max_block)
        prev: Optional[SmallHeaderBlock] = await rpc_client.get_header(max_block.prev_header_hash)
        if prev is not None:
            heads.append(prev)

    return added_blocks


async def stop_node(app):
    try:
        rpc_client: RpcClient = await RpcClient.create(app['config']['rpc_port'])
        await rpc_client.stop_node()
        rpc_client.close()

    except client_exceptions.ClientConnectorError:
        print("exception occured while stopping node")
