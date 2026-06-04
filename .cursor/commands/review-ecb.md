# Review ECB — 계약 위반 리뷰

MagicSquare_1004 **ECB·도메인 계약**만 읽기 전용으로 검사한다.  
**코드·테스트 수정 금지** — 위반 항목을 **표**로만 보고한다.

참고: `.cursorrules`, `Report/02`, `.cursor/skills/magic-square-tdd/reference.md`

---

## 필수 선언

**응답 첫 줄**에 반드시 선언한다.

```
Mode: Review ECB | Scope: src/ + tests/
```

사용자가 범위를 지정하면 `Scope:`에 반영 (예: `src/entity/`만).

---

## 절차

1. **범위 확인** — 기본: `src/entity`, `src/control`, `src/boundary`, `tests/entity`, `tests/control`, `tests/boundary`.
2. **파일 읽기** — `import` 문, 상수·리터럴, Mock 사용, 오류 코드 참조, 출력 형식만 스캔.
3. **체크 5항** — 아래 [체크리스트](#체크리스트) 각각 **Pass / Violation** 판정.
4. **표 작성** — Violation만 상세 행 추가; Pass는 요약 1행 또는 "위반 없음".
5. **보고** — [리뷰 결과 표](#리뷰-결과-표) + 총평 1~2문장. **수정 제안은 텍스트만**, 파일 편집 없음.

---

## 체크리스트

| # | 항목 | Pass 기준 | Violation 예 |
|---|------|-----------|--------------|
| C1 | **import 방향** | boundary→control→entity 단방향; entity는 외부 import **없음** | entity가 control/boundary import; control이 boundary import |
| C2 | **entity E001~E005** | entity에 `E001`~`E005` 문자열·enum·raise·분기 **없음** | entity에서 `raise E003`, `if code == "E001"` |
| C3 | **int[6] 1-index** | 출력·파싱·테스트 기대값이 `[r1,c1,n1,r2,c2,n2]`, 좌표 **1~4** | 0-index 좌표, 길이 ≠ 6, `(row,col)` 2-tuple만 반환 |
| C4 | **MagicConstant SSOT** | `34`, `16`, 격자 크기 `4`는 **단일 SSOT 모듈**에서만 정의·export | entity/control/boundary/tests에 `34`/`16` 리터럴 산재 |
| C5 | **Logic Track Domain Mock** | `tests/entity/`, `tests/control/`에서 `Mock`, `MagicMock`, `@patch`로 **도메인 함수·객체** 대역 **없음** | `@patch("entity.validate")`, `MagicMock()`으로 격자 대체 |

**부가 관찰** (Violation 표에 선택 기록):

- boundary 외 계층에서 `E006`~`E007` 정의
- control이 entity 우회해 도메인 로직 직접 구현
- `tests/boundary/`에서 I/O Mock — **허용** (C5 대상 아님)

---

## 리뷰 결과 표

위반 **0건**일 때:

| # | 체크 | 결과 | 파일 | 비고 |
|---|------|------|------|------|
| C1 | import 방향 | Pass | — | |
| C2 | entity E001~E005 | Pass | — | |
| C3 | int[6] 1-index | Pass | — | |
| C4 | MagicConstant SSOT | Pass | — | |
| C5 | Logic Domain Mock | Pass | — | |

**총평:** ECB·계약 위반 없음.

---

위반 **1건 이상**일 때 — Violation 행만 상세 기록:

| # | 체크 | 결과 | 파일:줄 | 위반 내용 |
|---|------|------|---------|-----------|
| C4 | MagicConstant SSOT | **Violation** | `src/entity/foo.py:12` | `MAGIC_SUM = 34` SSOT 외부 리터럴 |
| C1 | import 방향 | **Violation** | `src/entity/bar.py:3` | `from control import ...` |

Pass 항목은 `Pass` 한 줄로 묶어도 됨.

**총평:** Violation N건 — C1, C4 우선 수정 권고 (코드 변경은 사용자·GREEN/REFACTOR 턴에서).

---

## 스캔 힌트

```bash
# import (수동 검토용 — 실행만, 수정 없음)
rg "^from |^import " src/

# E001~E005 in entity
rg "E00[1-5]" src/entity/

# 리터럴 34 / 16
rg "\b34\b|\b16\b" src/ tests/

# Logic Track Mock
rg "Mock|MagicMock|@patch" tests/entity/ tests/control/
```

---

## 금지

- **`src/`·`tests/` 파일 수정** — 리뷰·표·총평만
- **자동 리팩터·GREEN 진행** — 위반 수정은 별도 TDD 턴
- **git commit** — 사용자 요청 시에만
- **범위 밖 품질 리뷰** — 네이밍·주석·성능 등 ECB·계약 외 항목은 언급 최소화
