# this file is generated by build_network_protocol_files.py

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from chia._tests.util.build_network_protocol_files import get_network_protocol_filename
from chia._tests.util.network_protocol_data import *  # noqa: F403
from chia._tests.util.protocol_messages_json import *  # noqa: F403


def parse_blob(input_bytes: bytes) -> Tuple[bytes, bytes]:
    size_bytes = input_bytes[:4]
    input_bytes = input_bytes[4:]
    size = int.from_bytes(size_bytes, "big")
    message_bytes = input_bytes[:size]
    input_bytes = input_bytes[size:]
    return (message_bytes, input_bytes)


def test_protocol_bytes() -> None:

    filename: Path = get_network_protocol_filename()
    assert filename.exists()
    with open(filename, "rb") as f:
        input_bytes = f.read()

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_0 = type(new_signage_point).from_bytes(message_bytes)
    assert message_0 == new_signage_point
    assert bytes(message_0) == bytes(new_signage_point)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_1 = type(declare_proof_of_space).from_bytes(message_bytes)
    assert message_1 == declare_proof_of_space
    assert bytes(message_1) == bytes(declare_proof_of_space)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_2 = type(request_signed_values).from_bytes(message_bytes)
    assert message_2 == request_signed_values
    assert bytes(message_2) == bytes(request_signed_values)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_3 = type(farming_info).from_bytes(message_bytes)
    assert message_3 == farming_info
    assert bytes(message_3) == bytes(farming_info)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_4 = type(signed_values).from_bytes(message_bytes)
    assert message_4 == signed_values
    assert bytes(message_4) == bytes(signed_values)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_5 = type(new_peak).from_bytes(message_bytes)
    assert message_5 == new_peak
    assert bytes(message_5) == bytes(new_peak)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_6 = type(new_transaction).from_bytes(message_bytes)
    assert message_6 == new_transaction
    assert bytes(message_6) == bytes(new_transaction)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_7 = type(request_transaction).from_bytes(message_bytes)
    assert message_7 == request_transaction
    assert bytes(message_7) == bytes(request_transaction)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_8 = type(respond_transaction).from_bytes(message_bytes)
    assert message_8 == respond_transaction
    assert bytes(message_8) == bytes(respond_transaction)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_9 = type(request_proof_of_weight).from_bytes(message_bytes)
    assert message_9 == request_proof_of_weight
    assert bytes(message_9) == bytes(request_proof_of_weight)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_10 = type(respond_proof_of_weight).from_bytes(message_bytes)
    assert message_10 == respond_proof_of_weight
    assert bytes(message_10) == bytes(respond_proof_of_weight)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_11 = type(request_block).from_bytes(message_bytes)
    assert message_11 == request_block
    assert bytes(message_11) == bytes(request_block)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_12 = type(reject_block).from_bytes(message_bytes)
    assert message_12 == reject_block
    assert bytes(message_12) == bytes(reject_block)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_13 = type(request_blocks).from_bytes(message_bytes)
    assert message_13 == request_blocks
    assert bytes(message_13) == bytes(request_blocks)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_14 = type(respond_blocks).from_bytes(message_bytes)
    assert message_14 == respond_blocks
    assert bytes(message_14) == bytes(respond_blocks)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_15 = type(reject_blocks).from_bytes(message_bytes)
    assert message_15 == reject_blocks
    assert bytes(message_15) == bytes(reject_blocks)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_16 = type(respond_block).from_bytes(message_bytes)
    assert message_16 == respond_block
    assert bytes(message_16) == bytes(respond_block)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_17 = type(new_unfinished_block).from_bytes(message_bytes)
    assert message_17 == new_unfinished_block
    assert bytes(message_17) == bytes(new_unfinished_block)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_18 = type(request_unfinished_block).from_bytes(message_bytes)
    assert message_18 == request_unfinished_block
    assert bytes(message_18) == bytes(request_unfinished_block)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_19 = type(respond_unfinished_block).from_bytes(message_bytes)
    assert message_19 == respond_unfinished_block
    assert bytes(message_19) == bytes(respond_unfinished_block)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_20 = type(new_signage_point_or_end_of_subslot).from_bytes(message_bytes)
    assert message_20 == new_signage_point_or_end_of_subslot
    assert bytes(message_20) == bytes(new_signage_point_or_end_of_subslot)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_21 = type(request_signage_point_or_end_of_subslot).from_bytes(message_bytes)
    assert message_21 == request_signage_point_or_end_of_subslot
    assert bytes(message_21) == bytes(request_signage_point_or_end_of_subslot)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_22 = type(respond_signage_point).from_bytes(message_bytes)
    assert message_22 == respond_signage_point
    assert bytes(message_22) == bytes(respond_signage_point)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_23 = type(respond_end_of_subslot).from_bytes(message_bytes)
    assert message_23 == respond_end_of_subslot
    assert bytes(message_23) == bytes(respond_end_of_subslot)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_24 = type(request_mempool_transaction).from_bytes(message_bytes)
    assert message_24 == request_mempool_transaction
    assert bytes(message_24) == bytes(request_mempool_transaction)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_25 = type(new_compact_vdf).from_bytes(message_bytes)
    assert message_25 == new_compact_vdf
    assert bytes(message_25) == bytes(new_compact_vdf)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_26 = type(request_compact_vdf).from_bytes(message_bytes)
    assert message_26 == request_compact_vdf
    assert bytes(message_26) == bytes(request_compact_vdf)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_27 = type(respond_compact_vdf).from_bytes(message_bytes)
    assert message_27 == respond_compact_vdf
    assert bytes(message_27) == bytes(respond_compact_vdf)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_28 = type(request_peers).from_bytes(message_bytes)
    assert message_28 == request_peers
    assert bytes(message_28) == bytes(request_peers)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_29 = type(respond_peers).from_bytes(message_bytes)
    assert message_29 == respond_peers
    assert bytes(message_29) == bytes(respond_peers)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_30 = type(new_unfinished_block2).from_bytes(message_bytes)
    assert message_30 == new_unfinished_block2
    assert bytes(message_30) == bytes(new_unfinished_block2)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_31 = type(request_unfinished_block2).from_bytes(message_bytes)
    assert message_31 == request_unfinished_block2
    assert bytes(message_31) == bytes(request_unfinished_block2)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_32 = type(request_puzzle_solution).from_bytes(message_bytes)
    assert message_32 == request_puzzle_solution
    assert bytes(message_32) == bytes(request_puzzle_solution)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_33 = type(puzzle_solution_response).from_bytes(message_bytes)
    assert message_33 == puzzle_solution_response
    assert bytes(message_33) == bytes(puzzle_solution_response)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_34 = type(respond_puzzle_solution).from_bytes(message_bytes)
    assert message_34 == respond_puzzle_solution
    assert bytes(message_34) == bytes(respond_puzzle_solution)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_35 = type(reject_puzzle_solution).from_bytes(message_bytes)
    assert message_35 == reject_puzzle_solution
    assert bytes(message_35) == bytes(reject_puzzle_solution)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_36 = type(send_transaction).from_bytes(message_bytes)
    assert message_36 == send_transaction
    assert bytes(message_36) == bytes(send_transaction)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_37 = type(transaction_ack).from_bytes(message_bytes)
    assert message_37 == transaction_ack
    assert bytes(message_37) == bytes(transaction_ack)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_38 = type(new_peak_wallet).from_bytes(message_bytes)
    assert message_38 == new_peak_wallet
    assert bytes(message_38) == bytes(new_peak_wallet)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_39 = type(request_block_header).from_bytes(message_bytes)
    assert message_39 == request_block_header
    assert bytes(message_39) == bytes(request_block_header)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_40 = type(request_block_headers).from_bytes(message_bytes)
    assert message_40 == request_block_headers
    assert bytes(message_40) == bytes(request_block_headers)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_41 = type(respond_header_block).from_bytes(message_bytes)
    assert message_41 == respond_header_block
    assert bytes(message_41) == bytes(respond_header_block)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_42 = type(respond_block_headers).from_bytes(message_bytes)
    assert message_42 == respond_block_headers
    assert bytes(message_42) == bytes(respond_block_headers)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_43 = type(reject_header_request).from_bytes(message_bytes)
    assert message_43 == reject_header_request
    assert bytes(message_43) == bytes(reject_header_request)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_44 = type(request_removals).from_bytes(message_bytes)
    assert message_44 == request_removals
    assert bytes(message_44) == bytes(request_removals)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_45 = type(respond_removals).from_bytes(message_bytes)
    assert message_45 == respond_removals
    assert bytes(message_45) == bytes(respond_removals)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_46 = type(reject_removals_request).from_bytes(message_bytes)
    assert message_46 == reject_removals_request
    assert bytes(message_46) == bytes(reject_removals_request)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_47 = type(request_additions).from_bytes(message_bytes)
    assert message_47 == request_additions
    assert bytes(message_47) == bytes(request_additions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_48 = type(respond_additions).from_bytes(message_bytes)
    assert message_48 == respond_additions
    assert bytes(message_48) == bytes(respond_additions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_49 = type(reject_additions).from_bytes(message_bytes)
    assert message_49 == reject_additions
    assert bytes(message_49) == bytes(reject_additions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_50 = type(request_header_blocks).from_bytes(message_bytes)
    assert message_50 == request_header_blocks
    assert bytes(message_50) == bytes(request_header_blocks)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_51 = type(reject_header_blocks).from_bytes(message_bytes)
    assert message_51 == reject_header_blocks
    assert bytes(message_51) == bytes(reject_header_blocks)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_52 = type(respond_header_blocks).from_bytes(message_bytes)
    assert message_52 == respond_header_blocks
    assert bytes(message_52) == bytes(respond_header_blocks)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_53 = type(coin_state).from_bytes(message_bytes)
    assert message_53 == coin_state
    assert bytes(message_53) == bytes(coin_state)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_54 = type(register_for_ph_updates).from_bytes(message_bytes)
    assert message_54 == register_for_ph_updates
    assert bytes(message_54) == bytes(register_for_ph_updates)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_55 = type(reject_block_headers).from_bytes(message_bytes)
    assert message_55 == reject_block_headers
    assert bytes(message_55) == bytes(reject_block_headers)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_56 = type(respond_to_ph_updates).from_bytes(message_bytes)
    assert message_56 == respond_to_ph_updates
    assert bytes(message_56) == bytes(respond_to_ph_updates)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_57 = type(register_for_coin_updates).from_bytes(message_bytes)
    assert message_57 == register_for_coin_updates
    assert bytes(message_57) == bytes(register_for_coin_updates)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_58 = type(respond_to_coin_updates).from_bytes(message_bytes)
    assert message_58 == respond_to_coin_updates
    assert bytes(message_58) == bytes(respond_to_coin_updates)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_59 = type(coin_state_update).from_bytes(message_bytes)
    assert message_59 == coin_state_update
    assert bytes(message_59) == bytes(coin_state_update)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_60 = type(request_children).from_bytes(message_bytes)
    assert message_60 == request_children
    assert bytes(message_60) == bytes(request_children)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_61 = type(respond_children).from_bytes(message_bytes)
    assert message_61 == respond_children
    assert bytes(message_61) == bytes(respond_children)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_62 = type(request_ses_info).from_bytes(message_bytes)
    assert message_62 == request_ses_info
    assert bytes(message_62) == bytes(request_ses_info)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_63 = type(respond_ses_info).from_bytes(message_bytes)
    assert message_63 == respond_ses_info
    assert bytes(message_63) == bytes(respond_ses_info)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_64 = type(coin_state_filters).from_bytes(message_bytes)
    assert message_64 == coin_state_filters
    assert bytes(message_64) == bytes(coin_state_filters)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_65 = type(request_add_puzzle_subscriptions).from_bytes(message_bytes)
    assert message_65 == request_add_puzzle_subscriptions
    assert bytes(message_65) == bytes(request_add_puzzle_subscriptions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_66 = type(respond_add_puzzle_subscriptions).from_bytes(message_bytes)
    assert message_66 == respond_add_puzzle_subscriptions
    assert bytes(message_66) == bytes(respond_add_puzzle_subscriptions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_67 = type(request_remove_puzzle_subscriptions).from_bytes(message_bytes)
    assert message_67 == request_remove_puzzle_subscriptions
    assert bytes(message_67) == bytes(request_remove_puzzle_subscriptions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_68 = type(respond_remove_puzzle_subscriptions).from_bytes(message_bytes)
    assert message_68 == respond_remove_puzzle_subscriptions
    assert bytes(message_68) == bytes(respond_remove_puzzle_subscriptions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_69 = type(request_add_coin_subscriptions).from_bytes(message_bytes)
    assert message_69 == request_add_coin_subscriptions
    assert bytes(message_69) == bytes(request_add_coin_subscriptions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_70 = type(respond_add_coin_subscriptions).from_bytes(message_bytes)
    assert message_70 == respond_add_coin_subscriptions
    assert bytes(message_70) == bytes(respond_add_coin_subscriptions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_71 = type(request_remove_coin_subscriptions).from_bytes(message_bytes)
    assert message_71 == request_remove_coin_subscriptions
    assert bytes(message_71) == bytes(request_remove_coin_subscriptions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_72 = type(respond_remove_coin_subscriptions).from_bytes(message_bytes)
    assert message_72 == respond_remove_coin_subscriptions
    assert bytes(message_72) == bytes(respond_remove_coin_subscriptions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_73 = type(request_reset_subscriptions).from_bytes(message_bytes)
    assert message_73 == request_reset_subscriptions
    assert bytes(message_73) == bytes(request_reset_subscriptions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_74 = type(respond_reset_subscriptions).from_bytes(message_bytes)
    assert message_74 == respond_reset_subscriptions
    assert bytes(message_74) == bytes(respond_reset_subscriptions)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_75 = type(request_puzzle_state).from_bytes(message_bytes)
    assert message_75 == request_puzzle_state
    assert bytes(message_75) == bytes(request_puzzle_state)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_76 = type(reject_puzzle_state).from_bytes(message_bytes)
    assert message_76 == reject_puzzle_state
    assert bytes(message_76) == bytes(reject_puzzle_state)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_77 = type(respond_puzzle_state).from_bytes(message_bytes)
    assert message_77 == respond_puzzle_state
    assert bytes(message_77) == bytes(respond_puzzle_state)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_78 = type(request_coin_state).from_bytes(message_bytes)
    assert message_78 == request_coin_state
    assert bytes(message_78) == bytes(request_coin_state)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_79 = type(respond_coin_state).from_bytes(message_bytes)
    assert message_79 == respond_coin_state
    assert bytes(message_79) == bytes(respond_coin_state)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_80 = type(pool_difficulty).from_bytes(message_bytes)
    assert message_80 == pool_difficulty
    assert bytes(message_80) == bytes(pool_difficulty)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_81 = type(harvester_handhsake).from_bytes(message_bytes)
    assert message_81 == harvester_handhsake
    assert bytes(message_81) == bytes(harvester_handhsake)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_82 = type(new_signage_point_harvester).from_bytes(message_bytes)
    assert message_82 == new_signage_point_harvester
    assert bytes(message_82) == bytes(new_signage_point_harvester)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_83 = type(new_proof_of_space).from_bytes(message_bytes)
    assert message_83 == new_proof_of_space
    assert bytes(message_83) == bytes(new_proof_of_space)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_84 = type(request_signatures).from_bytes(message_bytes)
    assert message_84 == request_signatures
    assert bytes(message_84) == bytes(request_signatures)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_85 = type(respond_signatures).from_bytes(message_bytes)
    assert message_85 == respond_signatures
    assert bytes(message_85) == bytes(respond_signatures)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_86 = type(plot).from_bytes(message_bytes)
    assert message_86 == plot
    assert bytes(message_86) == bytes(plot)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_87 = type(request_plots).from_bytes(message_bytes)
    assert message_87 == request_plots
    assert bytes(message_87) == bytes(request_plots)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_88 = type(respond_plots).from_bytes(message_bytes)
    assert message_88 == respond_plots
    assert bytes(message_88) == bytes(respond_plots)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_89 = type(request_peers_introducer).from_bytes(message_bytes)
    assert message_89 == request_peers_introducer
    assert bytes(message_89) == bytes(request_peers_introducer)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_90 = type(respond_peers_introducer).from_bytes(message_bytes)
    assert message_90 == respond_peers_introducer
    assert bytes(message_90) == bytes(respond_peers_introducer)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_91 = type(authentication_payload).from_bytes(message_bytes)
    assert message_91 == authentication_payload
    assert bytes(message_91) == bytes(authentication_payload)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_92 = type(get_pool_info_response).from_bytes(message_bytes)
    assert message_92 == get_pool_info_response
    assert bytes(message_92) == bytes(get_pool_info_response)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_93 = type(post_partial_payload).from_bytes(message_bytes)
    assert message_93 == post_partial_payload
    assert bytes(message_93) == bytes(post_partial_payload)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_94 = type(post_partial_request).from_bytes(message_bytes)
    assert message_94 == post_partial_request
    assert bytes(message_94) == bytes(post_partial_request)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_95 = type(post_partial_response).from_bytes(message_bytes)
    assert message_95 == post_partial_response
    assert bytes(message_95) == bytes(post_partial_response)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_96 = type(get_farmer_response).from_bytes(message_bytes)
    assert message_96 == get_farmer_response
    assert bytes(message_96) == bytes(get_farmer_response)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_97 = type(post_farmer_payload).from_bytes(message_bytes)
    assert message_97 == post_farmer_payload
    assert bytes(message_97) == bytes(post_farmer_payload)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_98 = type(post_farmer_request).from_bytes(message_bytes)
    assert message_98 == post_farmer_request
    assert bytes(message_98) == bytes(post_farmer_request)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_99 = type(post_farmer_response).from_bytes(message_bytes)
    assert message_99 == post_farmer_response
    assert bytes(message_99) == bytes(post_farmer_response)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_100 = type(put_farmer_payload).from_bytes(message_bytes)
    assert message_100 == put_farmer_payload
    assert bytes(message_100) == bytes(put_farmer_payload)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_101 = type(put_farmer_request).from_bytes(message_bytes)
    assert message_101 == put_farmer_request
    assert bytes(message_101) == bytes(put_farmer_request)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_102 = type(put_farmer_response).from_bytes(message_bytes)
    assert message_102 == put_farmer_response
    assert bytes(message_102) == bytes(put_farmer_response)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_103 = type(error_response).from_bytes(message_bytes)
    assert message_103 == error_response
    assert bytes(message_103) == bytes(error_response)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_104 = type(new_peak_timelord).from_bytes(message_bytes)
    assert message_104 == new_peak_timelord
    assert bytes(message_104) == bytes(new_peak_timelord)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_105 = type(new_unfinished_block_timelord).from_bytes(message_bytes)
    assert message_105 == new_unfinished_block_timelord
    assert bytes(message_105) == bytes(new_unfinished_block_timelord)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_106 = type(new_infusion_point_vdf).from_bytes(message_bytes)
    assert message_106 == new_infusion_point_vdf
    assert bytes(message_106) == bytes(new_infusion_point_vdf)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_107 = type(new_signage_point_vdf).from_bytes(message_bytes)
    assert message_107 == new_signage_point_vdf
    assert bytes(message_107) == bytes(new_signage_point_vdf)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_108 = type(new_end_of_sub_slot_bundle).from_bytes(message_bytes)
    assert message_108 == new_end_of_sub_slot_bundle
    assert bytes(message_108) == bytes(new_end_of_sub_slot_bundle)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_109 = type(request_compact_proof_of_time).from_bytes(message_bytes)
    assert message_109 == request_compact_proof_of_time
    assert bytes(message_109) == bytes(request_compact_proof_of_time)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_110 = type(respond_compact_proof_of_time).from_bytes(message_bytes)
    assert message_110 == respond_compact_proof_of_time
    assert bytes(message_110) == bytes(respond_compact_proof_of_time)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_111 = type(error_without_data).from_bytes(message_bytes)
    assert message_111 == error_without_data
    assert bytes(message_111) == bytes(error_without_data)

    message_bytes, input_bytes = parse_blob(input_bytes)
    message_112 = type(error_with_data).from_bytes(message_bytes)
    assert message_112 == error_with_data
    assert bytes(message_112) == bytes(error_with_data)

    assert input_bytes == b""
