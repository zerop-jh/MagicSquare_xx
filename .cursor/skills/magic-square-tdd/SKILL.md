---
name: magic-square-tdd
description: MagicSquare_1004 Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. TDD, RED/GREEN/REFACTOR, entity/control/boundary, D-*/U-* 테스트, validate, 마방진 34, ECB, MagicConstant SSOT 작업 시 사용.
---

# MagicSquare_1004 — Dual-Track TDD Skill

## 언제 이 Skill을 켜는가

다음 **하나 이상**에 해당하면 본 Skill을 적용한다.

- `src/entity`, `src/control`, `src/boundary` 또는 `tests/**` 코드·테스트를 **작성·수정**할 때
- 사용자가 **TDD**, **RED/GREEN/REFACTOR**, **D-***, **U-***, **ECB**, **Dual-Track**을 언급할 때
- `validate`, 마방합 34, 빈칸 2개, `int[6]` 출력, `E001`~`E007` 관련 작업 시
- MagicSquare_1004 **Logic Track** 또는 **UI Track** 구현·리팩터링 시

**켜지 않는 경우:** README·Report만 수정, git 작업만, Harness 골격 외 문서-only 요청.

시작 시 SSOT 확인: `.cursorrules` → `Report/02` → [reference.md](reference.md) (D-* ID).

---

## 턴 선언 (매 응답 필수)

```
Phase: RED | GREEN | REFACTOR
Layer: entity | control | boundary
Track: Logic (D-xxx) | UI (U-xxx)
```

---

## Logic Track vs UI Track

| | **Logic Track** | **UI Track** |
|---|-----------------|--------------|
| **대상** | entity, control | boundary |
| **테스트 ID** | `D-*` | `U-*` |
| **파일** | `tests/entity/test_d_*.py`, `tests/control/test_d_*.py` | `tests/boundary/test_u_*.py` |
| **Mock** | **Domain Mock 금지** | I/O·control **Mock 허용** |
| **순서** | entity → control 먼저 | boundary는 Logic GREEN 후 |
| **ECB import** | control→entity만 | boundary→control만 |

---

## ECB · Mock · 오류 코드

| 규칙 | entity | control | boundary |
|------|--------|---------|----------|
| import 방향 | **→ \* 금지** | entity만 | control만 |
| `E001`~`E005` | **처리 금지** | 변환·위임만 (도메인 예외→코드) | 정의·발생·매핑 |
| `E006`~`E007` | — | — | boundary 전담 |
| Domain Mock | **금지** | **금지** | — |
| I/O Mock | — | — | **허용** |
| MagicConstant `34`/`16` | SSOT 모듈만 | SSOT import | SSOT import |

---

## Phase: RED (5~7단계)

1. **ID 선정** — [reference.md](reference.md)에서 다음 `D-*` 또는 `U-*` 확인·등록.
2. **Layer·Track 확정** — entity부터; boundary는 Logic 선행 GREEN 필수.
3. **테스트 파일** — `test_d_<주제>.py` 또는 `test_u_<주제>.py`에 **함수 1개 = ID 1개**.
4. **Arrange** — 입력 격자·기대값을 도메인 규칙(4×4, 빈칸 2, 1-index)에 맞게 작성.
5. **Act·Assert** — 아직 없는 API를 호출; assert는 **엄격** (skip/xfail/완화 금지).
6. **실행** — 대상 테스트만 실행 → **FAIL 확인** (ImportError·AssertionError 허용, PASS는 RED 실패).
7. **보고** — 실패 메시지·원인 1줄; 구현 코드는 **아직 작성하지 않음**.

```bash
python -m pytest tests/entity/test_d_<name>.py -k "D-001" -v
```

---

## Phase: GREEN (5~7단계)

1. **RED 테스트 재확인** — 대상 `D-*`/`U-*`와 파일 일치 확인.
2. **최소 구현** — 해당 assert만 통과하는 **가장 짧은** 코드 (다른 ID 선행 구현 금지).
3. **Layer 준수** — entity에 I/O·E001~E005 넣지 않음; boundary에 도메인 로직 넣지 않음.
4. **MagicConstant** — `34`, `16`, 격자 크기 **리터럴 금지**; SSOT 모듈 사용.
5. **실행** — 대상 테스트만 → **PASS 확인**.
6. **부작용 검사** — 같은 파일 내 기존 테스트 깨지지 않았는지 해당 디렉터리 pytest.
7. **보고** — 통과한 ID·변경 파일 목록; REFACTOR 필요 여부 명시.

```bash
python -m pytest tests/entity/test_d_<name>.py -k "D-001" -v
python -m pytest tests/entity/ -v
```

---

## Phase: REFACTOR (5~7단계)

1. **GREEN 유지** — 리팩터 전 대상 Track pytest **전부 PASS** 스냅샷.
2. **범위 한정** — 동작 변경·새 ID·새 assert 추가 **금지** (새 ID는 RED로).
3. **중복 제거** — MagicConstant·10선 추출 등 SSOT/entity로 이동.
4. **ECB 경계** — import 위반·계층 누수 없는지 확인.
5. **실행** — 해당 Layer 디렉터리 전체 pytest → **전부 PASS**.
6. **Logic Track 완료 시** — `tests/entity/` + `tests/control/` 합산 실행.
7. **보고** — 리팩터 요약·변경 파일; 다음 RED 후보 ID 제안.

```bash
python -m pytest tests/entity/ tests/control/ -v
```

---

## Test / Review Loop

| 시점 | 명령 | 기대 |
|------|------|------|
| RED 직후 | `pytest <대상 파일> -k "<ID>" -v` | **FAIL** |
| GREEN 직후 | 동일 | **PASS** |
| REFACTOR 중 | `pytest tests/<layer>/ -v` | **전부 PASS** |
| control 작업 후 | `pytest tests/entity/ tests/control/ -v` | Logic 전부 PASS |
| boundary(U-*) RED/GREEN | `pytest tests/boundary/ -v` | Track별 PASS/FAIL |
| **완료 보고 전** | `python -m pytest` | **전체 PASS**, 수 초 이내 |
| 회귀 의심 시 | `python -m pytest -v --tb=short` | 실패 선·ID 특정 |

**금지:** `-x`로 실패 숨기기, `@pytest.mark.skip`, `xfail`, assert 완화 후 “통과” 보고.

---

## 완료 보고 항목

작업 턴 종료 시 아래를 **한국어**로 보고한다.

- [ ] **Phase / Layer / Track / ID** (예: `GREEN | entity | Logic | D-002`)
- [ ] **변경 파일** 목록 (`src/…`, `tests/…`)
- [ ] **pytest 결과** — 명령 + passed/failed 수
- [ ] **ECB 준수** — entity→\* 없음, E001~E005 entity 미사용
- [ ] **Mock 준수** — Logic Track Domain Mock 없음
- [ ] **MagicConstant** — 리터럴 34/16 새로 추가 없음
- [ ] **다음 ID** — reference.md 기준 다음 RED 후보

---

## 추가 참고

- D-* 테스트 ID 목록: [reference.md](reference.md)
- 프로젝트 규칙 SSOT: `.cursorrules`
- git commit·push: **사용자 요청 시에만**
