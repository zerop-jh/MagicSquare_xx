"""공통 pytest 픽스처 — 데이터만, 도메인 로직 없음."""

import importlib.util
import sys
import types
from pathlib import Path
from typing import Callable

import pytest

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
_ENTITY_PKG = _SRC / "entity"
_CONSTANTS_PATH = _ENTITY_PKG / "constants.py"
_LOCATION_PATH = _ENTITY_PKG / "location.py"
_SOLVER_PATH = _ENTITY_PKG / "solver.py"


def pytest_configure(config: pytest.Config) -> None:
    """tests/entity/ 와 src/entity 패키지 이름 충돌 방지."""
    config.option.importmode = "importlib"


def _ensure_src_entity_package() -> None:
    """tests/entity 패키지와 구분되도록 src/entity를 sys.modules에 등록."""
    if "entity" in sys.modules and getattr(sys.modules["entity"], "__path__", None):
        return
    pkg = types.ModuleType("entity")
    pkg.__path__ = [str(_ENTITY_PKG)]
    sys.modules["entity"] = pkg


def _load_entity_constants() -> object:
    """src/entity/constants.py SSOT — tests/entity 패키지 충돌 우회."""
    if "entity.constants" in sys.modules:
        return sys.modules["entity.constants"]
    _ensure_src_entity_package()
    spec = importlib.util.spec_from_file_location(
        "entity.constants",
        _CONSTANTS_PATH,
        submodule_search_locations=[str(_ENTITY_PKG)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load constants from {_CONSTANTS_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["entity.constants"] = module
    spec.loader.exec_module(module)
    return module


def _load_find_blank_coords() -> Callable[[list[list[int]]], list[tuple[int, int]]]:
    """src/entity/location.find_blank_coords — 패키지 충돌 우회."""
    _load_entity_constants()
    if "entity.location" in sys.modules:
        return sys.modules["entity.location"].find_blank_coords
    spec = importlib.util.spec_from_file_location(
        "entity.location",
        _LOCATION_PATH,
        submodule_search_locations=[str(_ENTITY_PKG)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load location from {_LOCATION_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["entity.location"] = module
    spec.loader.exec_module(module)
    return module.find_blank_coords


def _load_solve_step_a() -> Callable[[list[list[int]]], list[int]]:
    """src/entity/solver.solve_step_a — 패키지 충돌 우회."""
    _load_find_blank_coords()
    if "entity.solver" in sys.modules:
        return sys.modules["entity.solver"].solve_step_a
    spec = importlib.util.spec_from_file_location(
        "entity.solver",
        _SOLVER_PATH,
        submodule_search_locations=[str(_ENTITY_PKG)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load solver from {_SOLVER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["entity.solver"] = module
    spec.loader.exec_module(module)
    return module.solve_step_a


@pytest.fixture
def find_blank_coords() -> Callable[[list[list[int]]], list[tuple[int, int]]]:
    """D-LOC-01 Act — entity.find_blank_coords (실제 구현, Domain Mock 아님)."""
    return _load_find_blank_coords()


@pytest.fixture
def solve_step_a() -> Callable[[list[list[int]]], list[int]]:
    """D-SOL-01 Act — entity.solve_step_a (실제 구현, Domain Mock 아님)."""
    return _load_solve_step_a()


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
