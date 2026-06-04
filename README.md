# MagicSquare_1004

4×4 **부분 마방진** 학습 프로젝트. Mom Test로 문제를 정의하고, **10선 합 34 판정**(`validate`)부터 TDD로 구현한다.

---

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 도메인 | 4×4 격자, 빈칸 2개(`0`), 값 `1~16`, **마법합 34** |
| 검증 대상 | **10선** — 행 4 + 열 4 + 대각선 2 |
| 페르소나 | 4×4 부분 마방진을 손으로/코드로 다루는 **학습자** |
| 현재 단계 | STEP 1 (Mom Test) 완료 · **세션 3** (Rule + Command + Test Loop) 진행 예정 |

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
├── docs/
│   └── PRD.md                          # 제품 요구사항 (v0.1)
├── Report/
│   ├── 01.REPORT.md                    # STEP 1 Mom Test 인터뷰 보고서
│   └── 01.MagicSquare_ProblemDefinition_Report.md  # 문제 정의 통합 보고서
└── Prompting/
    ├── 01.mom_test_interview.md        # Mom Test 인터뷰 트랜스크립트
    └── 01.cursor_mom_test_workbook_discussion.md   # Cursor 대화 Export
```

> `src/`, `tests/` — 세션 3 구현 시 추가 예정 (`src/validator.py`, `tests/test_validator.py`)

---

## 로드맵

| 단계 | 내용 | 상태 |
|------|------|------|
| STEP 1 | Mom Test 인터뷰 · 문제 정의 | ✅ 완료 |
| 세션 3 | `validate` + Test Loop (TDD) | 🔲 진행 예정 |
| 이후 | MissingFinder, Solver, ECB Boundary | Out of scope |

---

## 성공 기준 (Acceptance Criteria)

| ID | 기준 | Mom Test |
|----|------|----------|
| AC-1 | 합 34가 **아닌** 격자 → `validate` = `False` | ③ “34가 안 맞아서” |
| AC-2 | 올바른 완성 마방진 → `validate` = `True` | 판정 기준선 |
| AC-3 | 빈칸 2개 부분 격자 처리 + 테스트 1건 | ② “빈칸 2개 넣었다” |
| AC-4 | `pytest` 1회, **수 초 이내** | ② “20분 헤맸다” |

---

## 실행 방법 (구현 후)

```bat
python -m venv .venv
.venv\Scripts\activate
pip install pytest
python -m pytest
```

구현 전에는 테스트·소스 코드가 없습니다. 세션 3에서 RED 테스트부터 작성합니다.

---

## 참고 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | 기능 요구사항, FR/AC, Test Loop |
| [Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md) | Mom Test + 문제 정의 + 세션 3 범위 |
| [Report/01.REPORT.md](Report/01.REPORT.md) | STEP 1 인터뷰 원본 보고서 |
| [Prompting/01.mom_test_interview.md](Prompting/01.mom_test_interview.md) | 인터뷰 트랜스크립트 |

---

## Mom Test 원칙 (인터뷰 시)

- ✅ “마지막으로 ~했을 때”, “몇 분 걸렸어?”, “뭐 때문에 포기했어?”
- ❌ “만들면 좋겠어?”, “이 기능 필요해?”, 솔루션 이름 먼저 제시

---

## 라이선스

학습용 프로젝트 (MagicSquare_1004)
