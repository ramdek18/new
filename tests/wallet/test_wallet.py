# flake8: noqa: F811, F401
import asyncio
import logging
import pytest

from src.consensus.block_rewards import calculate_base_farmer_reward, calculate_pool_reward
from src.protocols.full_node_protocol import RespondBlock
from src.server.server import ChiaServer
from src.simulator.simulator_protocol import FarmNewBlockProtocol, ReorgProtocol
from src.types.peer_info import PeerInfo
from src.util.ints import uint16, uint32
from src.wallet.util.transaction_type import TransactionType
from src.wallet.wallet_state_manager import WalletStateManager
from tests.fixtures import worker_number, worker_port
from tests.setup_nodes import self_hostname, setup_simulators_and_wallets
from tests.time_out_assert import time_out_assert, time_out_assert_not_none
from tests.wallet.cc_wallet.test_cc_wallet import tx_in_pool


@pytest.fixture(scope="module")
# @pytest.fixture(scope="function")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    # loop.close()


# return asyncio.get_event_loop()
# return asyncio.new_event_loop()

# @pytest.fixture#(scope="function") #(scope="module") #(scope="session")
# def event_loop():
#    loop = asyncio.get_event_loop()
#    yield loop


class TestWalletSimulator:
    @pytest.fixture(scope="function")
    async def wallet_node(self, worker_port):
        # todo: set plot_directories
        async for _ in setup_simulators_and_wallets(1, 1, {}, worker_port):
            yield _

    @pytest.fixture(scope="function")
    async def two_wallet_nodes(self, worker_port):
        async for _ in setup_simulators_and_wallets(1, 2, {}, worker_port):
            yield _

    @pytest.fixture(scope="function")
    async def two_wallet_nodes_five_freeze(self, worker_port):
        async for _ in setup_simulators_and_wallets(1, 2, {}, worker_port):
            yield _

    @pytest.fixture(scope="function")
    async def three_sim_two_wallets(self, worker_port):
        async for _ in setup_simulators_and_wallets(3, 2, {}, worker_port):
            yield _

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="temp. disabled while debugging test speedup")
    async def test_wallet_coinbase(self, wallet_node):
        num_blocks = 10
        full_nodes, wallets = wallet_node
        full_node_api = full_nodes[0]
        server_1: ChiaServer = full_node_api.full_node.server
        wallet_node, server_2 = wallets[0]

        wallet = wallet_node.wallet_state_manager.main_wallet
        ph = await wallet.get_new_puzzlehash()
        logging.info(f"Got puzzlehash {ph}")

        await server_2.start_client(PeerInfo(self_hostname, uint16(server_1._port)), None)
        for i in range(0, num_blocks):
            await full_node_api.farm_new_block(FarmNewBlockProtocol(ph))
        await full_node_api.farm_new_transaction_block(FarmNewBlockProtocol(ph))
        await full_node_api.farm_new_transaction_block(FarmNewBlockProtocol(ph))

        funds = sum(
            [
                calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i))
                for i in range(1, num_blocks + 2)
            ]
        )

        async def check_tx_are_pool_farm_rewards():
            wsm: WalletStateManager = wallet_node.wallet_state_manager
            all_txs = await wsm.get_all_transactions(1)
            expected_count = (num_blocks + 1) * 2
            if len(all_txs) != expected_count:
                return False
            pool_rewards = 0
            farm_rewards = 0

            for tx in all_txs:
                if tx.type == TransactionType.COINBASE_REWARD:
                    pool_rewards += 1
                elif tx.type == TransactionType.FEE_REWARD:
                    farm_rewards += 1

            if pool_rewards != expected_count / 2:
                return False
            if farm_rewards != expected_count / 2:
                return False
            return True

        await time_out_assert(10, check_tx_are_pool_farm_rewards, True)
        await time_out_assert(5, wallet.get_confirmed_balance, funds)

    @pytest.mark.asyncio
    async def test_wallet_make_transaction(self, two_wallet_nodes):
        num_blocks = 5
        full_nodes, wallets = two_wallet_nodes
        full_node_api = full_nodes[0]
        server_1 = full_node_api.full_node.server
        wallet_node, server_2 = wallets[0]
        wallet_node_2, server_3 = wallets[1]
        wallet = wallet_node.wallet_state_manager.main_wallet
        ph = await wallet.get_new_puzzlehash()

        await server_2.start_client(PeerInfo(self_hostname, uint16(server_1._port)), None)

        for i in range(0, num_blocks):
            await full_node_api.farm_new_transaction_block(FarmNewBlockProtocol(ph))

        funds = sum(
            [calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i)) for i in range(1, num_blocks)]
        )

        await time_out_assert(5, wallet.get_confirmed_balance, funds)
        await time_out_assert(5, wallet.get_unconfirmed_balance, funds)

        tx = await wallet.generate_signed_transaction(
            10,
            await wallet_node_2.wallet_state_manager.main_wallet.get_new_puzzlehash(),
            0,
        )
        print(tx)
        ret = await wallet.push_transaction(tx)
        print("---")
        print(ret)

        await time_out_assert(5, wallet.get_confirmed_balance, funds)
        await time_out_assert(5, wallet.get_unconfirmed_balance, funds - 10)

        for i in range(0, num_blocks):
            await full_node_api.farm_new_transaction_block(FarmNewBlockProtocol(ph))

        new_funds = sum(
            [
                calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i))
                for i in range(1, (2 * num_blocks))
            ]
        )

        await time_out_assert(5, wallet.get_confirmed_balance, new_funds - 10)
        await time_out_assert(5, wallet.get_unconfirmed_balance, new_funds - 10)

    """
    @pytest.mark.asyncio
    async def test_wallet_coinbase_reorg(self, wallet_node):
        num_blocks = 5
        full_nodes, wallets = wallet_node
        full_node_api = full_nodes[0]
        fn_server = full_node_api.full_node.server
        wallet_node, server_2 = wallets[0]
        wallet = wallet_node.wallet_state_manager.main_wallet
        ph = await wallet.get_new_puzzlehash()

        await server_2.start_client(PeerInfo(self_hostname, uint16(fn_server._port)), None)
        for i in range(0, num_blocks):
            await full_node_api.farm_new_transaction_block(FarmNewBlockProtocol(ph))

        funds = sum(
            [calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i)) for i in range(1, num_blocks)]
        )

        await time_out_assert(5, wallet.get_confirmed_balance, funds)

        await full_node_api.reorg_from_index_to_new_index(ReorgProtocol(uint32(3), uint32(num_blocks + 6), 32 * b"0"))

        funds = sum(
            [
                calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i))
                for i in range(1, num_blocks - 2)
            ]
        )

        await time_out_assert(5, wallet.get_confirmed_balance, funds)

    @pytest.mark.asyncio
    async def test_wallet_send_to_three_peers(self, three_sim_two_wallets):
        num_blocks = 10
        full_nodes, wallets = three_sim_two_wallets

        wallet_0, wallet_server_0 = wallets[0]
        full_node_api_0 = full_nodes[0]
        full_node_api_1 = full_nodes[1]
        full_node_api_2 = full_nodes[2]

        full_node_0 = full_node_api_0.full_node
        full_node_1 = full_node_api_1.full_node
        full_node_2 = full_node_api_2.full_node

        server_0 = full_node_0.server
        server_1 = full_node_1.server
        server_2 = full_node_2.server

        ph = await wallet_0.wallet_state_manager.main_wallet.get_new_puzzlehash()

        # wallet0 <-> sever0
        await wallet_server_0.start_client(PeerInfo(self_hostname, uint16(server_0._port)), None)

        for i in range(0, num_blocks):
            await full_node_api_0.farm_new_transaction_block(FarmNewBlockProtocol(ph))

        all_blocks = await full_node_api_0.get_all_full_blocks()

        for block in all_blocks:
            await full_node_1.respond_block(RespondBlock(block))
            await full_node_2.respond_block(RespondBlock(block))

        funds = sum(
            [calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i)) for i in range(1, num_blocks)]
        )

        await time_out_assert(5, wallet_0.wallet_state_manager.main_wallet.get_confirmed_balance, funds)

        tx = await wallet_0.wallet_state_manager.main_wallet.generate_signed_transaction(10, 32 * b"0", 0)
        await wallet_0.wallet_state_manager.main_wallet.push_transaction(tx)

        await time_out_assert_not_none(5, full_node_0.mempool_manager.get_spendbundle, tx.spend_bundle.name())

        # wallet0 <-> sever1
        await wallet_server_0.start_client(PeerInfo(self_hostname, uint16(server_1._port)), wallet_0.on_connect)

        await time_out_assert_not_none(5, full_node_1.mempool_manager.get_spendbundle, tx.spend_bundle.name())

        # wallet0 <-> sever2
        await wallet_server_0.start_client(PeerInfo(self_hostname, uint16(server_2._port)), wallet_0.on_connect)

        await time_out_assert_not_none(5, full_node_2.mempool_manager.get_spendbundle, tx.spend_bundle.name())

    @pytest.mark.asyncio
    async def test_wallet_make_transaction_hop(self, two_wallet_nodes_five_freeze):
        num_blocks = 10
        full_nodes, wallets = two_wallet_nodes_five_freeze
        full_node_api_0 = full_nodes[0]
        full_node_0 = full_node_api_0.full_node
        server_0 = full_node_0.server

        wallet_node_0, wallet_0_server = wallets[0]
        wallet_node_1, wallet_1_server = wallets[1]
        wallet_0 = wallet_node_0.wallet_state_manager.main_wallet
        wallet_1 = wallet_node_1.wallet_state_manager.main_wallet
        ph = await wallet_0.get_new_puzzlehash()

        await wallet_0_server.start_client(PeerInfo(self_hostname, uint16(server_0._port)), None)

        await wallet_1_server.start_client(PeerInfo(self_hostname, uint16(server_0._port)), None)

        for i in range(0, num_blocks):
            await full_node_api_0.farm_new_transaction_block(FarmNewBlockProtocol(ph))

        funds = sum(
            [calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i)) for i in range(1, num_blocks)]
        )

        await time_out_assert(5, wallet_0.get_confirmed_balance, funds)
        await time_out_assert(5, wallet_0.get_unconfirmed_balance, funds)

        assert await wallet_0.get_confirmed_balance() == funds
        assert await wallet_0.get_unconfirmed_balance() == funds

        tx = await wallet_0.generate_signed_transaction(
            10,
            await wallet_node_1.wallet_state_manager.main_wallet.get_new_puzzlehash(),
            0,
        )

        await wallet_0.push_transaction(tx)

        # Full node height 11, wallet height 9
        await time_out_assert(5, wallet_0.get_confirmed_balance, funds)
        await time_out_assert(5, wallet_0.get_unconfirmed_balance, funds - 10)

        for i in range(0, 4):
            await full_node_api_0.farm_new_transaction_block(FarmNewBlockProtocol(32 * b"0"))

        # here it's num_blocks + 1 because our last reward is included in the first block that we just farmed
        new_funds = sum(
            [
                calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i))
                for i in range(1, num_blocks + 1)
            ]
        )

        # Full node height 17, wallet height 15
        await time_out_assert(5, wallet_0.get_confirmed_balance, new_funds - 10)
        await time_out_assert(5, wallet_0.get_unconfirmed_balance, new_funds - 10)
        await time_out_assert(5, wallet_1.get_confirmed_balance, 10)

        tx = await wallet_1.generate_signed_transaction(5, await wallet_0.get_new_puzzlehash(), 0)
        await wallet_1.push_transaction(tx)

        for i in range(0, 4):
            await full_node_api_0.farm_new_transaction_block(FarmNewBlockProtocol(32 * b"0"))

        await wallet_0.get_confirmed_balance()
        await wallet_0.get_unconfirmed_balance()
        await wallet_1.get_confirmed_balance()

        await time_out_assert(5, wallet_0.get_confirmed_balance, new_funds - 5)
        await time_out_assert(5, wallet_0.get_unconfirmed_balance, new_funds - 5)
        await time_out_assert(5, wallet_1.get_confirmed_balance, 5)

    # @pytest.mark.asyncio
    # async def test_wallet_finds_full_node(self):
    #     node_iters = [
    #         setup_full_node(
    #             test_constants,
    #             "blockchain_test.db",
    #             11234,
    #             introducer_port=11236,
    #             simulator=False,
    #         ),
    #         setup_wallet_node(
    #             11235,
    #             test_constants,
    #             None,
    #             introducer_port=11236,
    #         ),
    #         setup_introducer(11236),
    #     ]
    #
    #     full_node_api = await node_iters[0].__anext__()
    #     wallet, wallet_server = await node_iters[1].__anext__()
    #     introducer, introducer_server = await node_iters[2].__anext__()
    #
    #     async def has_full_node():
    #         outbound: List[WSChiaConnection] = wallet.server.get_outgoing_connections()
    #         for connection in outbound:
    #             if connection.connection_type is NodeType.FULL_NODE:
    #                 return True
    #         return False
    #
    #     await time_out_assert(
    #         2 * 60,
    #         has_full_node,
    #         True,
    #     )
    #     await _teardown_nodes(node_iters)

    @pytest.mark.asyncio
    async def test_wallet_make_transaction_with_fee(self, two_wallet_nodes):
        num_blocks = 5
        full_nodes, wallets = two_wallet_nodes
        full_node_1 = full_nodes[0]
        wallet_node, server_2 = wallets[0]
        wallet_node_2, server_3 = wallets[1]
        wallet = wallet_node.wallet_state_manager.main_wallet
        ph = await wallet.get_new_puzzlehash()

        await server_2.start_client(PeerInfo(self_hostname, uint16(full_node_1.full_node.server._port)), None)

        for i in range(0, num_blocks):
            await full_node_1.farm_new_transaction_block(FarmNewBlockProtocol(ph))

        funds = sum(
            [calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i)) for i in range(1, num_blocks)]
        )

        await time_out_assert(5, wallet.get_confirmed_balance, funds)
        await time_out_assert(5, wallet.get_unconfirmed_balance, funds)

        assert await wallet.get_confirmed_balance() == funds
        assert await wallet.get_unconfirmed_balance() == funds
        tx_amount = 3200000000000
        tx_fee = 10
        tx = await wallet.generate_signed_transaction(
            tx_amount,
            await wallet_node_2.wallet_state_manager.main_wallet.get_new_puzzlehash(),
            tx_fee,
        )

        fees = tx.spend_bundle.fees()
        assert fees == tx_fee

        await wallet.push_transaction(tx)

        await time_out_assert(5, wallet.get_confirmed_balance, funds)
        await time_out_assert(5, wallet.get_unconfirmed_balance, funds - tx_amount - tx_fee)

        for i in range(0, num_blocks):
            await full_node_1.farm_new_transaction_block(FarmNewBlockProtocol(32 * b"0"))

        new_funds = sum(
            [
                calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i))
                for i in range(1, num_blocks + 1)
            ]
        )

        await time_out_assert(5, wallet.get_confirmed_balance, new_funds - tx_amount - tx_fee)
        await time_out_assert(5, wallet.get_unconfirmed_balance, new_funds - tx_amount - tx_fee)

    @pytest.mark.asyncio
    async def test_wallet_create_hit_max_send_amount(self, two_wallet_nodes):
        num_blocks = 5
        full_nodes, wallets = two_wallet_nodes
        full_node_1 = full_nodes[0]
        wallet_node, server_2 = wallets[0]
        wallet_node_2, server_3 = wallets[1]
        wallet = wallet_node.wallet_state_manager.main_wallet
        ph = await wallet.get_new_puzzlehash()

        await server_2.start_client(PeerInfo(self_hostname, uint16(full_node_1.full_node.server._port)), None)

        for i in range(0, num_blocks):
            await full_node_1.farm_new_transaction_block(FarmNewBlockProtocol(ph))

        funds = sum(
            [calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i)) for i in range(1, num_blocks)]
        )

        await time_out_assert(5, wallet.get_confirmed_balance, funds)

        primaries = []
        for i in range(0, 600):
            primaries.append({"puzzlehash": ph, "amount": 100000000 + i})

        tx_split_coins = await wallet.generate_signed_transaction(1, ph, 0, primaries=primaries)

        await wallet.push_transaction(tx_split_coins)
        await time_out_assert(
            15, tx_in_pool, True, full_node_1.full_node.mempool_manager, tx_split_coins.spend_bundle.name()
        )
        for i in range(0, num_blocks):
            await full_node_1.farm_new_transaction_block(FarmNewBlockProtocol(32 * b"0"))

        funds = sum(
            [
                calculate_pool_reward(uint32(i)) + calculate_base_farmer_reward(uint32(i))
                for i in range(1, num_blocks + 1)
            ]
        )

        await time_out_assert(90, wallet.get_confirmed_balance, funds)
        max_sent_amount = await wallet.get_max_send_amount()

        # 1) Generate transaction that is under the limit
        under_limit_tx = None
        try:
            under_limit_tx = await wallet.generate_signed_transaction(
                max_sent_amount - 1,
                ph,
                0,
            )
        except ValueError:
            assert ValueError

        assert under_limit_tx is not None

        # 2) Generate transaction that is equal to limit
        at_limit_tx = None
        try:
            at_limit_tx = await wallet.generate_signed_transaction(
                max_sent_amount,
                ph,
                0,
            )
        except ValueError:
            assert ValueError

        assert at_limit_tx is not None

        # 3) Generate transaction that is greater than limit
        above_limit_tx = None
        try:
            above_limit_tx = await wallet.generate_signed_transaction(
                max_sent_amount + 1,
                ph,
                0,
            )
        except ValueError:
            pass

        assert above_limit_tx is None
"""
