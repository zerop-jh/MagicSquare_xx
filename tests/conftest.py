"""공통 pytest 픽스처 — 데이터만, 도메인 로직 없음."""

import importlib.util
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
_CONSTANTS_PATH = _SRC / "entity" / "constants.py"


def pytest_configure(config: pytest.Config) -> None:
    """tests/entity/ 와 src/entity 패키지 이름 충돌 방지."""
    config.option.importmode = "importlib"


def _load_entity_constants() -> object:
    """src/entity/constants.py SSOT — tests/entity 패키지 충돌 우회."""
    spec = importlib.util.spec_from_file_location(
        "entity_constants",
        _CONSTANTS_PATH,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load constants from {_CONSTANTS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """G1: 4×4, 빈칸(`0`) 2개 — (2,2), (3,3) 1-index, row-major."""
    constants = _load_entity_constants()
    grid_size = constants.GRID_SIZE

    grid = [
        [16, 3, 2, 13],
        [5, 0, 11, 12],
        [9, 6, 0, 12],
        [4, 15, 14, 1],
    ]
    if len(grid) != grid_size or any(len(row) != grid_size for row in grid):
        raise ValueError("G1 must be GRID_SIZE x GRID_SIZE")
    return grid
