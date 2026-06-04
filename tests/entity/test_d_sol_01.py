"""D-SOL-01 — solve_step_a int[6] (FR-SOL-01) + Golden Master."""

import sys
from collections.abc import Callable
from pathlib import Path

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))

from _approval import assert_matches_golden

_GOLDEN_D_SOL_01_G1_STEP_A = "d_sol_01_g1_step_a.approved.txt"


def test_d_sol_01_step_a_success(
    grid_g1: list[list[int]],
    solve_step_a: Callable[[list[list[int]]], list[int]],
) -> None:
    # Given: G1 격자 (빈칸 2개)
    # When: solve_step_a(grid_g1) 호출
    # Then: int[6] 1-index — Golden Master 승인
    result = solve_step_a(grid_g1)
    assert len(result) == 6
    assert_matches_golden(result, _GOLDEN_D_SOL_01_G1_STEP_A)
