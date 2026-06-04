# TDD RED — 실패 테스트 먼저

MagicSquare_1004 Dual-Track TDD **RED 단계만** 수행한다.  
`tests/`에 실패하는 테스트를 작성하고 pytest FAIL을 확인한다. **구현(`src/`)은 하지 않는다.**

참고: `.cursorrules`, `.cursor/skills/magic-square-tdd/reference.md` (D-* / U-* ID)

---

## 필수 선언

**응답 첫 줄**에 반드시 선언한다.

```
Phase: RED | Layer: entity | Track: Logic (D-001)
```

| 필드 | 값 |
|------|-----|
| Phase | `RED` (소문자 `red` 허용) |
| Layer | `entity` \| `control` \| `boundary` |
| Track | `Logic (D-xxx)` \| `UI (U-xxx)` |

---

## 절차

1. **ID 확인** — `reference.md`에서 다음 `D-*`(Logic) 또는 `U-*`(UI) ID·Layer·Track 확정.  
   - Logic: entity → control 순. boundary(U-*)는 Logic 선행 GREEN 후.
2. **파일 배치** — Logic: `tests/entity/test_d_*.py` 또는 `tests/control/test_d_*.py`  
   UI: `tests/boundary/test_u_*.py`  
   함수 1개 = ID 1개. 테스트명·docstring에 ID 포함 (예: `test_d001_sum_line`).
3. **AAA 테스트 작성**
   - **Arrange** — 4×4 격자, 빈칸 0×2, 값 1~16, 1-index 좌표 규칙 준수.
   - **Act** — 아직 없는 `src/` API 호출 (ImportError·AttributeError는 RED FAIL로 유효).
   - **Assert** — 기대값 **엄격**히 명시. `skip`·`xfail`·assert 완화 금지.
4. **pytest 실행** — 대상 ID만 실행 → **FAIL 확인**. PASS면 RED 실패(테스트·기대값 재검토).
5. **보고** — 아래 [보고](#보고) 형식. `src/` 미변경 확인.

---

## pytest 예시

```bash
# Logic Track — entity, 단일 ID
python -m pytest tests/entity/test_d_sum_line.py -k "D-001" -v

# Logic Track — control
python -m pytest tests/control/test_d_validate.py -k "D-006" -v

# UI Track — boundary
python -m pytest tests/boundary/test_u_parse_input.py -k "U-001" -v

# RED 확인: exit code != 0, FAILED 또는 ImportError/AssertionError
python -m pytest tests/entity/test_d_sum_line.py::test_d001_sum_line -v
```

**RED 성공 기준:** pytest **FAIL** (ImportError · AssertionError · FAILED).  
**RED 실패:** pytest **PASS** (구현이 이미 있거나 assert가 너무 약함).

---

## 보고

RED 턴 종료 시 **한국어**로 다음만 보고한다.

| 항목 | 내용 |
|------|------|
| 테스트 ID | `D-001` 또는 `U-001` |
| FAIL 요약 | pytest 출력 1~3줄 (예: `ImportError: cannot import name 'sum_line'`) |
| 변경 파일 | **`tests/` 하위만** — 경로 목록 |

예:

```
Phase: RED | Layer: entity | Track: Logic (D-001)
- ID: D-001
- FAIL: ImportError — sum_line 미구현
- 변경: tests/entity/test_d_sum_line.py
```

---

## 금지

- **`src/` 수정** — entity / control / boundary 구현·스텁·`__init__.py` export 추가 금지
- **Logic Track Domain Mock** — entity·control 테스트에서 도메인 객체·함수 Mock 금지
- **assert 완화** — `assert result is not None`, `pytest.skip`, `pytest.mark.xfail`, try/except로 assert 우회 금지
- **GREEN·REFACTOR** — 본 Command 범위 밖; 사용자가 별도 요청할 때까지 진행하지 않음
- **git commit** — 사용자 요청 시에만
