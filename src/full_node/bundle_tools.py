from clvm import SExp
from clvm_tools import binutils

from src.types.blockchain_format.program import NilSerializedProgram, SerializedProgram
from src.types.spend_bundle import SpendBundle
from typing import Tuple


def best_solution_program(bundle: SpendBundle) -> Tuple[SerializedProgram, SerializedProgram]:
    """
    This could potentially do a lot of clever and complicated compression
    optimizations in conjunction with choosing the set of SpendBundles to include.

    For now, we just quote the solutions we know.
    """
    r = []
    for coin_solution in bundle.coin_solutions:
        entry = [coin_solution.coin.name(), [coin_solution.puzzle_reveal, coin_solution.solution]]
        r.append(entry)
    return (SerializedProgram.from_bytes(SExp.to((binutils.assemble("#q"), r)).as_bin()), NilSerializedProgram)
