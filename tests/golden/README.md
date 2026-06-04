# Golden Master — Logic Track 기준선

GREEN PASS 직후 **승인된 입·출력** 스냅샷. REFACTOR·회귀 시 동일 기대값을 유지한다.

| 파일 | Test ID | 내용 |
|------|---------|------|
| `d_loc_01_g1_baseline.json` | D-LOC-01 | G1 → `[(2,2), (3,3)]` (1-index, row-major) |
| `d_sol_01_g1_step_a.approved.txt` | D-SOL-01 | G1 `solve_step_a` → `INT6: 2,2,6,3,3,7` |

pytest assert SSOT는 `tests/entity/test_d_*.py`이며, `.approved.txt`는 `tests/_approval.py` + `UPDATE_GOLDEN=1`로만 갱신한다.
