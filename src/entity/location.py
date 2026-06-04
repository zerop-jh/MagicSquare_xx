"""빈칸 좌표 등 격자 위치 도메인 로직."""

from entity.constants import BLANK_CELL, GRID_SIZE


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """빈칸(`BLANK_CELL`) 좌표를 row-major, 1-index (row, col) 튜플 목록으로 반환."""
    coords: list[tuple[int, int]] = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == BLANK_CELL:
                coords.append((row + 1, col + 1))
    return coords
