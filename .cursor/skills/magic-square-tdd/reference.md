# D-* Logic Track 테스트 ID

| ID | Layer | 주제 | AC/FR |
|----|-------|------|-------|
| D-001 | entity | `sum_line` — 한 줄(행/열/대각) 합 계산 | FR-2 |
| D-002 | entity | `validate` — 합 ≠ 34 격자 → `False` | AC-1 |
| D-003 | entity | `validate` — 완성 마방진 → `True` | AC-2 |
| D-004 | entity | `validate` — 빈칸 2개 부분 격자 정책 | AC-3 |
| D-005 | entity | 격자 크기·값 범위 위반 → `False` | F3 |
| D-006 | control | entity `validate` 오케스트레이션 | FR-1 |
| D-007 | entity | MagicConstant SSOT — 리터럴 34/16 미사용 | `.cursorrules` |
| D-LOC-01 | entity | `find_blank_coords` — G1 빈칸 좌표 row-major 1-index | FR-LOC-01 · **GREEN PASS** |

> U-* ID는 boundary Track 착수 시 `test_u_*.py`와 함께 추가한다.
