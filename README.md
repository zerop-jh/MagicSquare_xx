# MagicSquare_1004

4×4 **부분 마방진** 학습 프로젝트. Mom Test로 문제를 정의하고, **10선 합 34 판정**(`validate`)부터 TDD로 구현한다.

---

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 도메인 | 4×4 격자, 빈칸 2개(`0`), 값 `1~16`, **마법합 34** |
| 검증 대상 | **10선** — 행 4 + 열 4 + 대각선 2 |
| 페르소나 | 4×4 부분 마방진을 손으로/코드로 다루는 **학습자** |
| 현재 단계 | STEP 1~3 완료 · **RED 단계** (Dual-Track TDD) 진행 중 |

### 진짜 문제 (Mom Test)

> 4×4 부분 마방진에서 빈 칸 2개를 채운 뒤 10선(행·열·대각선) 합(34)이 맞는지 바로 판정하지 못해, 한 번의 시도만으로도 20분 가까이 시행착오를 반복한다.

### Mom Test 증거

1. “4×4 부분 마방진을 손으로/코드로 다루는 학습자”
2. “지난번에 빈칸 2개 넣었다가 … **20분 헤맸다**”
3. “**34가 안 맞아서**”

---

## 도메인 규칙

```
┌────┬────┬────┬────┐
│ 16 │  3 │  2 │ 13 │  ← 각 행 합 = 34
├────┼────┼────┼────┤
│  5 │ 10 │ 11 │  ? │  ← 빈칸 2개 (0)
├────┼────┼────┼────┤
│  9 │  6 │  ? │ 12 │
├────┼────┼────┼────┤
│  4 │ 15 │ 14 │  1 │
└────┴────┴────┴────┘
  ↑ 열·대각선도 각각 합 34
```

| 규칙 | 설명 |
|------|------|
| R1 | 격자 4×4 |
| R2 | 셀 값: `0`(빈칸) 또는 `1~16` |
| R3 | 마법합 = **34** |
| R4 | 10선 각각 합 34 |
| R5 | 완성 시 1~16 중복 없음 |

---

## 범위

### 이번 세션 (세션 3) — 만드는 것

| 8계층 | 산출물 |
|--------|--------|
| **Rule** | 도메인 규칙 (위 표) |
| **Command** | `validate(grid)` — 10선 합 34 판정 |
| **(Skill)** | 실패 선 식별 *(선택)* |
| **Test Loop** | RED → GREEN → REFACTOR |

### 하지 않는 것 (Non-Goals)

- Solver — 빈칸 자동 채우기
- MissingFinder — 빈칸 위치 탐색
- GridUI / InputHandler / ResultDisplay
- ECB 전체 아키텍처 완성

> **표면 문제:** “Solver·Validator 프로그램을 만들면 빈칸 2개를 빠르게 채울 수 있다.”  
> → 본 프로젝트 v0.1은 **판정(`validate`)만** 다룬다.

---

## 프로젝트 구조

```
MagicSquare_xx/
├── README.md
├── .cursorrules
├── pyproject.toml
├── docs/
│   ├── PRD.md                          # 제품 요구사항 (v0.1)
│   └── TODO.md                         # Dual-Track TDD To Do (상세)
├── src/
│   ├── entity/                         # Logic Track
│   ├── control/
│   └── boundary/                       # UI Track
├── tests/
│   ├── entity/                         # test_d_*.py
│   ├── control/
│   └── boundary/                       # test_u_*.py
├── Report/                             # STEP 1~3 보고서
└── .cursor/skills/magic-square-tdd/    # TDD Skill, D-* reference
```

---

## RED 단계 체크리스트

> 상세: [docs/TODO.md](docs/TODO.md) · Command: `/tdd-red` · **Logic(B) 먼저** → Boundary(A)는 Logic GREEN 완료 후

### 진행 순서

```
Track B (Logic)     D-001 → D-007   RED (tests/ only, pytest FAIL)
       ↓ Logic GREEN 완료 후
Track A (Boundary)  U-IN → U-OUT → U-FLOW   RED
```

### Track B — Logic RED (`D-*`)

**규칙:** `tests/`만 변경 · `src/` 수정 금지 · Domain Mock 금지 · RED 성공 = pytest **FAIL**

#### entity

- [ ] **D-001** — `sum_line` 한 줄 합 (FR-2) · `tests/entity/test_d_sum_line.py`
  - Given: 행1 `[16, 3, 2, 13]` → Then: `sum_line(cells) == 34` → Expected RED: `ImportError`
- [ ] **D-002** — 합≠34 → `False` (AC-1) · `tests/entity/test_d_validate.py`
  - Given: G_bad → Then: `validate(grid) == False` → Expected RED: `ImportError` / `AssertionError`
- [ ] **D-003** — 완성 마방진 → `True` (AC-2)
  - Given: G_complete → Then: `validate(grid) == True` → Expected RED: `ImportError` / `AssertionError`
- [ ] **D-004** — 빈칸 2개 부분 격자 (AC-3)
  - Given: G_partial → Then: 정책에 따른 `validate` 결과 → Expected RED: `ImportError` / `AssertionError`
- [ ] **D-005** — 크기·값 범위 위반 → `False` (F3)
  - Given: 3×4 또는 범위 위반 → Then: `validate(grid) == False` → Expected RED: `ImportError` / `AssertionError`
- [ ] **D-007** — MagicConstant SSOT
  - Given: SSOT 모듈 → Then: `34`, `16` 리터럴 없이 참조 → Expected RED: `ImportError` / `AssertionError`
  - 파일: `tests/entity/test_d_magic_constant.py`

#### control

- [ ] **D-006** — `validate` 오케스트레이션 (FR-1) · `tests/control/test_d_validate.py`
  - Given: G_complete → Then: control 경유 `validate` → `True` → Expected RED: `ImportError` / `AssertionError`

### Track A — Boundary RED (`U-*`)

> **선행:** Track B Logic GREEN 완료 · I/O·control Mock 허용

#### 입력 (U-IN)

- [ ] **U-IN-01** — `grid=None` → `E003 INVALID_NULL` → Expected RED: `ModuleNotFoundError`
- [ ] **U-IN-02** — `grid=3×4` → `E001 INVALID_SIZE` → Expected RED: `AssertionError`
- [ ] **U-IN-03** — 빈칸 0개 → `E002 INVALID_BLANK` → Expected RED: `AssertionError`

#### 출력·흐름 (U-OUT / U-FLOW)

- [ ] **U-OUT-01** — 유효 입력 G1 → `len(result) == 6` (`int[6]`, 1-index) → Expected RED: `pytest.fail()`
- [ ] **U-FLOW-02** — `grid=None` → `execute()` 0회 호출 → Expected RED: `pytest.fail()`

파일: `tests/boundary/test_u_*.py`

---

## 로드맵

| 단계 | 내용 | 상태 |
|------|------|------|
| STEP 1 | Mom Test 인터뷰 · 문제 정의 | ✅ 완료 |
| STEP 2 | Harness · ECB · `.cursorrules` | ✅ 완료 |
| STEP 3 | Skill · Command (`/tdd-red`, `/review-ecb`) | ✅ 완료 |
| **RED** | Logic `D-*` → Boundary `U-*` 실패 테스트 | 🔲 진행 중 |
| GREEN / REFACTOR | 최소 구현 · 리팩터 | 🔲 대기 |
| 이후 | MissingFinder, Solver, GridUI | Out of scope |

---

## 성공 기준 (Acceptance Criteria)

| ID | 기준 | Mom Test |
|----|------|----------|
| AC-1 | 합 34가 **아닌** 격자 → `validate` = `False` | ③ “34가 안 맞아서” |
| AC-2 | 올바른 완성 마방진 → `validate` = `True` | 판정 기준선 |
| AC-3 | 빈칸 2개 부분 격자 처리 + 테스트 1건 | ② “빈칸 2개 넣었다” |
| AC-4 | `pytest` 1회, **수 초 이내** | ② “20분 헤맸다” |

---

## 실행 방법

```bat
cd c:\DEV\MagicSquare_xx
python -m pip install -e ".[dev]"
python -m pytest tests/entity/test_d_sum_line.py -k "D-001" -v
```

RED 단계에서는 대상 테스트가 **FAIL**이어야 합니다 (`ImportError` · `AssertionError` · `FAILED`).

---

## 참고 문서

| 문서 | 설명 |
|------|------|
| [docs/TODO.md](docs/TODO.md) | Dual-Track TDD To Do · RED/GREEN 마일스톤 |
| [docs/PRD.md](docs/PRD.md) | 기능 요구사항, FR/AC, Test Loop |
| [Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md) | Mom Test + 문제 정의 |
| [Report/02.MagicSquare_Harness_Setup_Report.md](Report/02.MagicSquare_Harness_Setup_Report.md) | Harness · ECB · Dual-Track |
| [Report/03.MagicSquare_Skill_Command_Report.md](Report/03.MagicSquare_Skill_Command_Report.md) | Skill · `/tdd-red` · D-* ID |

---

## Mom Test 원칙 (인터뷰 시)

- ✅ “마지막으로 ~했을 때”, “몇 분 걸렸어?”, “뭐 때문에 포기했어?”
- ❌ “만들면 좋겠어?”, “이 기능 필요해?”, 솔루션 이름 먼저 제시

---

## 라이선스

학습용 프로젝트 (MagicSquare_1004)
