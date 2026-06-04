"""Golden Master 승인 비교 — int[6]·에러 코드 포맷 고정."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Sequence, Union

import pytest

_GOLDEN_ROOT = Path(__file__).resolve().parent / "golden"

Actual = Union[Sequence[int], str]


def format_for_golden(actual: Actual) -> str:
    """승인 파일 한 줄 포맷 (수동 편집·우회 금지 — UPDATE_GOLDEN으로만 갱신)."""
    if isinstance(actual, str):
        text = actual.strip()
        if text.startswith("ERROR:"):
            return text
        return f"ERROR: {text}"
    values = list(actual)
    if len(values) != 6:
        raise ValueError(f"int[6] expected, got len={len(values)}: {values!r}")
    parts = ",".join(str(int(v)) for v in values)
    return f"INT6: {parts}"


def assert_matches_golden(actual: Actual, relative: str) -> None:
    """actual을 golden 파일과 비교. UPDATE_GOLDEN=1 이면 기준 파일 갱신."""
    golden_path = _GOLDEN_ROOT / relative
    rendered = format_for_golden(actual)

    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(rendered + "\n", encoding="utf-8")
        return

    if not golden_path.is_file():
        pytest.fail(f"golden missing: {golden_path} (run UPDATE_GOLDEN=1 once)")

    expected = golden_path.read_text(encoding="utf-8").strip()
    if rendered != expected:
        pytest.fail(
            f"golden mismatch: {golden_path}\n"
            f"  expected: {expected!r}\n"
            f"  actual:   {rendered!r}"
        )
