"""빈칸 채움(Solver) — Logic Track D-SOL."""

from entity.constants import GRID_SIZE, MAGIC_SUM
from entity.location import find_blank_coords


def solve_step_a(grid: list[list[int]]) -> list[int]:
    """G1 등 부분 격자: 빈칸 2곳 row-major 1-index + 행 합 기준 채움값 → int[6]."""
    coords = find_blank_coords(grid)
    if len(coords) != 2:
        raise ValueError("solve_step_a requires exactly two blank cells")

    r1, c1 = coords[0]
    r2, c2 = coords[1]
    row1 = grid[r1 - 1]
    row2 = grid[r2 - 1]
    n1 = MAGIC_SUM - sum(row1[j] for j in range(GRID_SIZE) if j != c1 - 1)
    n2 = MAGIC_SUM - sum(row2[j] for j in range(GRID_SIZE) if j != c2 - 1)
    return [r1, c1, n1, r2, c2, n2]
