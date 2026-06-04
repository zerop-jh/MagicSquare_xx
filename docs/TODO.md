# MagicSquare_1004 — Dual-Track TDD To Do List

> RED 설계표 기준 작업 목록. Logic Track(B)을 **먼저** GREEN까지 완료한 뒤 Boundary Track(A)을 착수한다.  
> SSOT: `.cursorrules`, `.cursor/skills/magic-square-tdd/reference.md`, `docs/PRD.md`

---

## 진행 순서

```
Track B (Logic)  D-001 → D-007  RED → GREEN → REFACTOR
       ↓ Logic GREEN 완료 후
Track A (Boundary)  U-IN → U-OUT → U-FLOW  RED → GREEN → REFACTOR
```

| Track | Layer | 테스트 ID | 파일 패턴 | Mock |
|-------|-------|-----------|-----------|------|
| **Logic (B)** | entity, control | `D-*` | `tests/entity/test_d_*.py`, `tests/control/test_d_*.py` | Domain Mock **금지** |
| **Boundary (A)** | boundary | `U-*` | `tests/boundary/test_u_*.py` | I/O·control Mock **허용** |

---

## Track B — Logic RED To Do List

**Layer:** `entity` / `control` · **Command:** `/tdd-red`

### entity — `sum_line` · `validate` · SSOT

- [ ] **D-001** — `sum_line` 한 줄 합 계산 (FR-2)
  - **Given:** 한 줄 cells (예: 행1 `[16, 3, 2, 13]`)
  - **Then:** `sum_line(cells) == 34`
  - **Expected RED:** `ImportError`
  - **파일:** `tests/entity/test_d_sum_line.py`

- [ ] **D-002** — 합≠34 격자 → `False` (AC-1, Mom Test ③)
  - **Given:** 합≠34 격자 G_bad
  - **Then:** `validate(grid) == False`
  - **Expected RED:** `ImportError` / `AssertionError`
  - **파일:** `tests/entity/test_d_validate.py`

- [ ] **D-003** — 완성 4×4 마방진 → `True` (AC-2)
  - **Given:** 완성 4×4 마방진 G_complete
  - **Then:** `validate(grid) == True`
  - **Expected RED:** `ImportError` / `AssertionError`
  - **파일:** `tests/entity/test_d_validate.py`

- [ ] **D-004** — 빈칸 2개 부분 격자 정책 (AC-3, Mom Test ②)
  - **Given:** 빈칸 2개 부분 격자 G_partial
  - **Then:** 정책에 따른 `validate` 결과
  - **Expected RED:** `ImportError` / `AssertionError`
  - **파일:** `tests/entity/test_d_validate.py`

- [ ] **D-005** — 크기·값 범위 위반 → `False` (F3)
  - **Given:** 3×4 격자 또는 값 범위 위반
  - **Then:** `validate(grid) == False`
  - **Expected RED:** `ImportError` / `AssertionError`
  - **파일:** `tests/entity/test_d_validate.py`

- [ ] **D-007** — MagicConstant SSOT (`.cursorrules`)
  - **Given:** MagicConstant SSOT 모듈
  - **Then:** `34`, `16` 리터럴 없이 SSOT 참조
  - **Expected RED:** `ImportError` / `AssertionError`
  - **파일:** `tests/entity/test_d_magic_constant.py`

### control — 오케스트레이션

- [ ] **D-006** — entity `validate` 오케스트레이션 (FR-1)
  - **Given:** 유효 격자 G_complete
  - **Then:** control 경유 `validate` → `True`
  - **Expected RED:** `ImportError` / `AssertionError`
  - **파일:** `tests/control/test_d_validate.py`

### Logic Track 마일스톤

- [ ] D-001~D-005, D-007 entity RED 테스트 작성 및 pytest **FAIL** 확인
- [ ] D-001~D-005, D-007 entity GREEN — 최소 구현 후 pytest **PASS**
- [ ] D-006 control RED → GREEN
- [ ] REFACTOR — `tests/entity/` + `tests/control/` 전체 pytest **PASS**
- [ ] `/review-ecb` — Logic Track ECB 계약 검증 (C1~C5)

---

## Track A — Boundary RED To Do List

> **선행 조건:** Track B Logic GREEN 완료

**Layer:** `boundary` · **Command:** `/tdd-red`

### 입력 검증 (U-IN)

- [ ] **U-IN-01** — `None` 입력
  - **Given:** `grid=None`
  - **Then:** `E003 INVALID_NULL`
  - **Expected RED:** `ModuleNotFoundError`

- [ ] **U-IN-02** — 잘못된 격자 크기
  - **Given:** `grid=3×4`
  - **Then:** `E001 INVALID_SIZE`
  - **Expected RED:** `AssertionError`

- [ ] **U-IN-03** — 빈칸 개수 위반
  - **Given:** 빈칸 0개
  - **Then:** `E002 INVALID_BLANK`
  - **Expected RED:** `AssertionError`

### 출력 검증 (U-OUT)

- [ ] **U-OUT-01** — 유효 입력 출력 형식
  - **Given:** 유효 입력 G1
  - **Then:** `len(result) == 6` (`int[6]`, 1-index `[r1,c1,n1,r2,c2,n2]`)
  - **Expected RED:** `pytest.fail()` RED

### 흐름 검증 (U-FLOW)

- [ ] **U-FLOW-02** — 입력 실패 시 control 미호출
  - **Given:** `grid=None`
  - **Then:** `execute()` 0회 호출
  - **Expected RED:** `pytest.fail()` RED

### Boundary Track 마일스톤

- [ ] U-IN-01~03 RED 테스트 작성 (`tests/boundary/test_u_*.py`) 및 pytest **FAIL** 확인
- [ ] U-OUT-01, U-FLOW-02 RED 테스트 작성 및 pytest **FAIL** 확인
- [ ] Boundary GREEN — 최소 구현 후 pytest **PASS**
- [ ] REFACTOR — `tests/boundary/` 전체 pytest **PASS**
- [ ] `/review-ecb` — Boundary 포함 전체 ECB 검증

---

## 오류 코드 참조 (Boundary)

| 코드 | 의미 | 관련 U-* |
|------|------|----------|
| E001 | `INVALID_SIZE` — 4×4 아님 | U-IN-02 |
| E002 | `INVALID_BLANK` — 빈칸(`0`)이 2개가 아님 | U-IN-03 |
| E003 | `INVALID_NULL` — 입력 `None` | U-IN-01, U-FLOW-02 |
| E004~E007 | boundary 전담 (추후 정의) | — |

> entity는 `E001`~`E005` 처리 **금지** — 도메인 불변식·판정만 담당.

---

## RED 단계 공통 규칙

- [ ] 매 턴 선언: `Phase: RED | Layer: ... | Track: ...`
- [ ] RED 중 **`src/` 수정 금지** — `tests/`만 변경
- [ ] assert 완화·`skip`·`xfail` **금지**
- [ ] Logic Track **Domain Mock 금지**
- [ ] RED 성공 기준: pytest **FAIL** (`ImportError` · `AssertionError` · `FAILED`)

---

## 완료 기준 (전체)

- [ ] `python -m pytest` — **전체 PASS**, 수 초 이내 (AC-4)
- [ ] MagicConstant `34`/`16` 리터럴 산재 없음 (SSOT)
- [ ] ECB import 방향: boundary → control → entity, entity → \* 금지

---

## 참고

| 문서 | 설명 |
|------|------|
| [PRD.md](PRD.md) | FR/AC, 도메인 규칙 |
| [../.cursor/skills/magic-square-tdd/reference.md](../.cursor/skills/magic-square-tdd/reference.md) | D-* ID 순서 |
| [../.cursor/commands/tdd-red.md](../.cursor/commands/tdd-red.md) | RED Command 절차 |
| [../Report/03.REPORT.md](../Report/03.REPORT.md) | STEP 3 Skill·Command 요약 |
