# MagicSquare_1004 — PRD (Product Requirements Document)

## 1. 문서 개요

| 항목 | 내용 |
|------|------|
| 제품 | MagicSquare_1004 |
| 버전 | 0.1 (초안) |
| 기준 | Mom Test STEP 1 + 세션 3 워크북 |
| 목적 | 진짜 문제(합 34 판정·확인 비용) 해결을 위한 **최소 검증 기능** 정의 |

---

## 2. 배경 및 문제

### 페르소나

4×4 부분 마방진(빈칸 2개·0, 1~16, 합 34)을 손으로/코드로 다루는 **학습자**

### 진짜 문제

4×4 부분 마방진에서 빈 칸 2개를 채운 뒤 10선(행·열·대각선) 합(34)이 맞는지 바로 판정하지 못해, 한 번의 시도만으로도 20분 가까이 시행착오를 반복한다.

### Mom Test 증거

1. “4×4 부분 마방진을 손으로/코드로 다루는 학습자”
2. “지난번에 빈칸 2개 넣었다가 … **20분 헤맸다**”
3. “**34가 안 맞아서**”

### 표면 문제 (Non-Goal)

“ECB Solver·Validator 프로그램을 만들면 빈칸 2개를 빠르게 채우고 합 34를 맞출 수 있다.” — **본 PRD의 목표가 아님**

---

## 3. 제품 목표

### Goal

학습자가 빈칸 2개를 채운 4×4 격자에 대해, **10선 합 34 여부를 즉시 판정**할 수 있게 한다.

### Non-Goals (v0.1)

- 빈칸 자동 채우기 (Solver)
- 빈칸 위치 탐색 (MissingFinder)
- GUI (GridUI, InputHandler, ResultDisplay)
- ECB 전체 아키텍처 완성
- 힌트·자동 교정·학습 추천

---

## 4. R-G-I-O

| | 설명 |
|---|------|
| **Role** | 부분 마방진을 풀며 “합이 맞나?”를 확인해야 하는 학습자 |
| **Goal** | 10선 합 34 충족 여부를 빠르게 알기 |
| **Input** | `grid: list[list[int]]` — 4×4, 값 `0` 또는 `1~16`, 빈칸 2개 |
| **Output** | `bool` — `True`(유효) / `False`(무효) · *(v0.2)* 실패 선 목록 |

---

## 5. 도메인 규칙 (Rule)

| ID | 규칙 |
|----|------|
| R1 | 격자 크기는 4×4 |
| R2 | 셀 값은 `0`(빈칸) 또는 `1~16` |
| R3 | **마법합 = 34** |
| R4 | **10선** — 행 4, 열 4, 대각선 2 — 각각 합 34 |
| R5 | 완성 격자: 1~16 각각 1회 (중복 없음) |
| R6 | 부분 격자: `0`이 포함된 줄은 v0.1에서 **검사 제외** 또는 **정책 명시 후 부분 검사** *(구현 시 택1)* |

### 실패 조건 (문제 인식점)

- F1: 10선 중 하나라도 합 ≠ 34
- F2: 완성 격자에서 1~16 중복 또는 누락
- F3: 격자 크기 ≠ 4×4 또는 값 범위 위반

---

## 6. 기능 요구사항

### FR-1: `validate(grid) -> bool`

| 항목 | 내용 |
|------|------|
| 설명 | 4×4 격자가 마방진 조건(10선 합 34, R5)을 만족하는지 판정 |
| 우선순위 | P0 (세션 3 필수) |
| Mom Test | ③ “34가 안 맞아서” → 틀린 격자에서 `False` |

### FR-2: `sum_line(cells) -> int` *(내부)*

| 항목 | 내용 |
|------|------|
| 설명 | 한 줄(행/열/대각)의 합 계산 |
| 우선순위 | P0 |
| Mom Test | ② 확인 비용 절감의 기초 연산 |

### FR-3: 실패 선 식별 *(선택, v0.2)*

| 항목 | 내용 |
|------|------|
| 설명 | `False`일 때 10선 중 합 ≠ 34인 선 반환 |
| 우선순위 | P2 |
| Mom Test | ③ 어느 선에서 틀렸는지 학습자에게 전달 |

---

## 7. 성공 기준 (Acceptance Criteria)

| ID | 기준 | Mom Test |
|----|------|----------|
| AC-1 | 합 34가 **아닌** 격자 입력 시 `validate` → `False`, 테스트 Fail | ③ |
| AC-2 | 올바른 4×4 완성 마방진 입력 시 `validate` → `True` | 판정 기준선 |
| AC-3 | 빈칸 2개(0) 부분 격자 처리 정책 문서화 + 테스트 1건 | ② |
| AC-4 | `pytest` 1회 실행으로 AC-1~3 검증, **수 초 이내** | ② “20분 헤맸다” |

---

## 8. 테스트 요구사항 (Test Loop)

### RED (먼저 작성)

```text
test_validate_returns_false_when_sum_not_34  # 증거 ③
test_validate_returns_true_for_complete_magic_square
test_validate_handles_partial_grid_two_blanks  # 증거 ②
```

### GREEN

- `src/validator.py` (또는 동등 모듈)에 `validate` 최소 구현

### REFACTOR

- 10선 합산 중복 제거 (범위 허용 시)

---

## 9. 8계층 매핑 (세션 3)

| 계층 | PRD 대응 |
|------|----------|
| Rule | §5 도메인 규칙 |
| Command | FR-1 `validate`, FR-2 `sum_line` |
| (Skill) | FR-3 실패 선 식별 |
| Test Loop | §8 |

---

## 10. 범위 및 로드맵

| 단계 | 범위 | 상태 |
|------|------|------|
| STEP 1 | Mom Test · 문제 정의 | 완료 |
| 세션 3 | Rule + Command + Test Loop | **현재** |
| 이후 | MissingFinder, Solver, ECB Boundary | Out of scope |

---

## 11. 참고 문서

- `Report/01.MagicSquare_ProblemDefinition_Report.md`
- `Report/01.REPORT.md`
- `Prompting/01.mom_test_interview.md`
