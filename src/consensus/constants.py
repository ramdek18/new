from typing import Any, Dict

constants: Dict[str, Any] = {
    "NUMBER_OF_HEADS": 3,  # The number of tips each full node keeps track of and propagates
    "DIFFICULTY_STARTING": 17179869184,  # 2^34. These are in units of 2^32
    "DIFFICULTY_FACTOR": 3,  # The next difficulty is truncated to range [prev / FACTOR, prev * FACTOR]
    # These 3 constants must be changed at the same time
    "DIFFICULTY_EPOCH": 128,  # The number of blocks per epoch
    "DIFFICULTY_WARP_FACTOR": 4,  # DELAY divides EPOCH in order to warp efficiently.
    "DIFFICULTY_DELAY": 32,  # EPOCH / WARP_FACTOR
    "SIGNIFICANT_BITS": 12,  # The number of bits to look at in difficulty and min iters. The rest are zeroed
    "DISCRIMINANT_SIZE_BITS": 1024,  # Max is 1024 (based on ClassGroupElement int size)
    "BLOCK_TIME_TARGET": 300,  # The target number of seconds per block
    # The proportion (denominator) of the total time that that the VDF must be run for, at a minimum
    # (1/min_iters_proportion). For example, if this is two, approximately half of the iterations
    # will be contant and required for all blocks.
    "MIN_ITERS_PROPORTION": 10,
    # For the first epoch, since we have no previous blocks, we can't estimate vdf iterations per second
    "MIN_ITERS_STARTING": (2 ** 17),
    "MAX_FUTURE_TIME": 7200,  # The next block can have a timestamp of at most these many seconds more
    "NUMBER_OF_TIMESTAMPS": 11,  # Than the average of the last NUMBEBR_OF_TIMESTAMPS blocks
    # If an unfinished block is more than these many seconds slower than the best unfinished block,
    # don't propagate it.
    "PROPAGATION_THRESHOLD": 300,
    # If the expected time is more than these seconds, slightly delay the propagation of the unfinished
    # block, to allow better leaders to be released first. This is a slow block.
    "PROPAGATION_DELAY_THRESHOLD": 1500,
    # Hardcoded genesis block, generated using tests/block_tools.py
    # Replace this any time the constants change.
    "GENESIS_BLOCK": b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x15N3\xd3\xf9H\xc2K\x96\xfe\xf2f\xa2\xbf\x87\x0e\x0f,\xd0\xd4\x0f6s\xb1".\\\xf5\x8a\xb4\x03\x84\x8e\xf9\xbb\xa1\xca\xdef3:\xe4?\x0c\xe5\xc6\x12\x80\x88\xbe_6 X\xf1\x83\xe8\x99\xdf)\xb8\xf6t\xe0;\x82\x17\xc5\xe5\x94\xb7\xef\xc2|\x94\xe6\xfb\x91L\x85\xe4\x00WVV\xefJ\x1e/>\xf6\xc5Gr5n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00^\x9d\x942\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00o\xc4O\x915\x18\x9b]\'\x13\x8d\x1c\xa9\xd3\xb2D\x10+\xbb\xd5 \x13\x9fa\x91<\xc1\x1b\xd9\x19\x0f\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x8b)\xaa\x96x8\xd76J\xa6\x8b[\x98\t\xe0\\\xe3^7qD\x8c\xf5q\x08\xf2\xa2\xc9\xb03mv\x00\x00\x0c\xbb\xa1\x06\xe0\x00N\x1f\xe8;}6F\xd7\xec\xc7\x83\x16T\x96\x1f\xe6\x88,\xa4\x9b\xa3Lo\xd0\xe6\x89jW\xac\xba\xae)\xe9\x91?\x97\x0fU\xf5\xd8\xdc\x9e\xce\xbf~\xad\xc2\xbc\x17v|\x947N\x0e\xfa\xff\xe6;\xce@|\xe9{\xe2:\xa8H\xb4\xb9\xde;<;-\x9a\x03\xbf\xa3\xff\xed\x81\x0cd\x80|(I\x9e\x8c\xa5\x83\xdf\x8a\x1aX\x8c\xb9\x01%\x17\xc8\x17\xfe\xade\x02\x87\xd6\x1b\xdd\x9ch\x80;k\xf9\xc6A3\xdc\xab>e\xb5\xa5\x0c\xb9\x8b)\xaa\x96x8\xd76J\xa6\x8b[\x98\t\xe0\\\xe3^7qD\x8c\xf5q\x08\xf2\xa2\xc9\xb03mv\x00\x00\x01\xd1\xa9J \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$)\xcf\x82\xc23&\xedzR\x04\xb8Zz\xe9\x03\x94\xe1\x0f\xc2\xe1TS\xc2\xb6\xd1\xa5\xf2\xd6\xb4\xae\xfb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc7D\xa6H\x1c\x9a\x1c\xd5O\x8e\xe6\x9bI\xf4""\x05I\xe6\xf5io\xb0N\xb0\xcf9\x96\xad\x8e\x01\x81\xd6\xb2\x7f\x19\x1c\xf5\x95\x06\x9a\x8eR1\xff[\x98\x05\x07\xe4\xb3\x10A\xe71eZ\xb8\xa6\x9a\xbcY\xaa\xb0\xe2\xda#B\x8c\r\xea*u\x90\xe1mdrU\x12#\x7f\xa8\r#\xe2V\xc2\x07\xe9i8\xe2\xbd\xfa\x1c\x00\x00',  # noqa: E501
    # Target tx count per sec
    "TX_PER_SEC": 20,
    # Size of mempool = 10x the size of block
    "MEMPOOL_BLOCK_BUFFER": 10,
    # Coinbase rewards are not spendable for 200 blocks
    "COINBASE_FREEZE_PERIOD": 200,
    # Max coin amount uint(1 << 64)
    "MAX_COIN_AMOUNT": b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF",
    # Raw size per block target = 1,000,000 bytes
    # Rax TX (single in, single out) = 219 bytes (not compressed)
    # TX = 457 vBytes
    # floor(1,000,000 / 219) * 457 = 2086662 (size in vBytes)
    # Max block cost in virtual bytes
    "MAX_BLOCK_COST": 2086662,
    # MAX block cost in clvm cost units = MAX_BLOCK_COST * CLVM_COST_RATIO_CONSTANT
    # 1 vByte = 108 clvm cost units
    "CLVM_COST_RATIO_CONSTANT": 108,
    # Max block cost in clvm cost units (MAX_BLOCK_COST * CLVM_COST_RATIO_CONSTANT)
    "MAX_BLOCK_COST_CLVM": 225359496,
}
