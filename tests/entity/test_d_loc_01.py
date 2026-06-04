"""D-LOC-01 — blank_coords row-major (FR-LOC-01)."""

from collections.abc import Callable


def test_d_loc_01_blank_coords_row_major(
    grid_g1: list[list[int]],
    find_blank_coords: Callable[[list[list[int]]], list[tuple[int, int]]],
) -> None:
    # Given: G1 격자 (0이 2개)
    # When: find_blank_coords(grid_g1) 호출
    # Then: [(2, 2), (3, 3)] 반환 (1-index, row-major)
    assert find_blank_coords(grid_g1) == [(2, 2), (3, 3)]
