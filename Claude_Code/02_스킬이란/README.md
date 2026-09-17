# skill-creator로 PRD 스킬 만들기 실습 진행 순서

## 1. 실습 환경 준비

- Windows + VS Code + Git Bash에서 진행한다.
- [1회차](../Claude_1회차_CLI_설치와_계정_연결하기/README.md)의 Claude Code 설치와 Pro 계정 연결을 완료한다.
- 이번 회차에서는 기능 요청을 PRD로 정리하는 스킬을 만든다. 앱 코드는 작성하지 않으므로 빈 폴더에서 시작할 수 있다.
- 2~4회차에서 사용할 공통 실습 폴더를 준비한다. 아래 명령으로 홈 폴더에 `claude-code-practice` 폴더를 만들고 VS Code로 연다.

Git Bash에서 실행한다.

```bash
mkdir -p ~/claude-code-practice
cd ~/claude-code-practice
mkdir -p .claude/skills
code .
claude --version
claude
```

폴더 신뢰 확인이 나오면 방금 만든 실습 폴더인지 확인하고 승인한다. Claude Code에서 연결 상태를 확인한다.

```text
/status
```

## 2. 스킬과 PRD 이해하기

- **스킬**: 반복해서 사용하는 지침과 절차를 묶어 둔 파일이다.
- **description**: 스킬을 언제 사용할지 설명하는 항목이다. Claude는 이 설명과 요청 내용을 바탕으로 스킬 사용 여부를 판단한다.
- **본문**: Claude가 스킬을 사용할 때 따르는 구체적인 작업 절차다.
- **PRD(Product Requirements Document)**: 만들 기능의 목적과 요구사항을 정리한 문서다. 이번 실습에서는 구현 전에 아래 여섯 항목을 정리한다.

| 항목 | 확인할 내용 |
|---|---|
| 배경 | 왜 필요한가 |
| 목적 | 무엇을 해결하는가 |
| 범위 | 이번에 포함하고 제외할 것은 무엇인가 |
| 요구사항 | 어떤 동작을 만족해야 하는가 |
| 절차 | 어떤 순서로 작업하는가 |
| 완료조건 | 어떤 결과를 확인하면 작업이 완료되었다고 판단하는가 |

이번에 만들 스킬의 이름은 `prd-feature`다. 기능 요청을 받으면 PRD를 먼저 작성하고, 사용자가 승인한 뒤에 구현하도록 지침을 작성한다. 호출 실습에서는 PRD를 작성한 뒤 구현하지 않고 승인을 기다리는지 확인한다.

## 3. skill-creator 설치

Claude Code에서 실행한다.

```text
/plugin install skill-creator@claude-plugins-official
```

- 설치 범위를 묻는다면 **User scope**를 선택한다. 현재 사용자 계정에서 사용할 수 있는 범위다.
- 이미 설치되어 있다면 `/plugin`의 Installed(설치됨) 목록에서 활성화 상태를 확인한다.
- 설치 결과에 `Run /reload-plugins to activate.`가 나오면 아래 명령을 실행한다.

```text
/reload-plugins
```

변경 사항이 반영되지 않거나 명령을 사용할 수 없다면 `/exit`로 종료하고 Git Bash에서 `claude`를 다시 실행한다.

공식 마켓플레이스를 찾지 못할 때만 아래 명령을 실행한 뒤 설치를 재시도한다.

```text
/plugin marketplace add anthropics/claude-plugins-official
```

## 4. PRD 스킬 만들기

### 제작 시작

Claude Code에서 아래 요청을 입력한다.

```text
/skill-creator:skill-creator prd-feature라는 프로젝트 스킬을 만들고 싶어. 짧고 모호한 기능 요청을 받으면 바로 코드를 작성하지 않고 PRD를 먼저 정리하는 스킬이야. 한국어로 필요한 질문을 해줘. 결과는 현재 폴더의 .claude/skills/prd-feature/SKILL.md에 만들어줘. 기존 파일이 있으면 덮어쓰기 전에 확인받아줘.
```

### 인터뷰 답변

skill-creator가 스킬의 용도와 동작을 질문하면 아래 내용을 바탕으로 답변한다. 질문 순서와 문구는 실행할 때마다 달라질 수 있다.

```text
스킬의 역할은 기능 구현 전에 배경, 목적, 범위(포함/제외), 요구사항, 절차, 완료조건을 정리하는 것이야.
"기능 만들어줘", "이거 구현해줘"처럼 짧고 모호한 기능 요청에 사용해줘.
"오타 하나만 고쳐줘"처럼 이미 구체적인 단순 수정 요청에는 자동으로 사용하지 않도록 설명해줘.
정보가 부족하면 필요한 질문을 하고, 확인되지 않은 프로젝트 상태는 사실처럼 쓰지 말아줘.
결과는 여섯 항목을 갖춘 한국어 마크다운 PRD로 보여줘.
PRD를 보여준 뒤 멈추고 사용자 확인을 받아줘. 구현 승인을 받은 뒤에만 구현을 시작하도록 해줘.
이번에는 스킬 파일을 만들고 직접 호출해서 동작을 확인할 거야. 자동 평가, 벤치마크, Python 스크립트 실행, 패키징은 생략해줘.
TODO 앱 코드는 만들지 말고 스킬 파일만 만들어줘.
```

- 파일 생성이나 수정에 대한 승인을 요청하면 대상 경로가 공통 실습 폴더 안인지 확인한 뒤 승인한다.
- 결과 파일이 다른 경로에 생겼다면 지정한 프로젝트 스킬 경로로 옮겨 달라고 요청한다.

## 5. 생성된 스킬 확인

VS Code 탐색기에서 `.claude/skills/prd-feature/SKILL.md`를 연다.

파일 맨 위에서 `---`로 둘러싸인 영역을 **frontmatter**라고 한다. 스킬의 이름과 사용 조건 같은 정보를 적는 부분이다.

- 파일 첫 줄이 `---`인지 확인한다.
- frontmatter에 `name: prd-feature`와 사용 조건을 담은 `description`이 있는지 확인한다.
- 본문에 PRD 여섯 항목과 구현 전 확인 절차가 있는지 확인한다.
- `disable-model-invocation: true`가 있으면 자동 호출이 제한되고, `user-invocable: false`가 있으면 직접 호출 메뉴에 표시되지 않는다. 이번에는 두 호출 방식을 모두 사용하므로 해당 설정이 있으면 제거해 달라고 요청한다.

아래 예시와 비교해 이름과 사용 조건이 들어 있는지 확인한다. 설명 문구까지 같을 필요는 없다.

```yaml
---
name: prd-feature
description: >-
  짧고 모호한 기능 요청을 구현하기 전에 PRD로 정리한다.
  "기능 만들어줘", "이거 구현해줘"처럼 요구사항 구체화가 필요한 요청에 사용한다.
  오타 수정처럼 구체적인 단순 수정 요청에는 사용하지 않는다.
---
```

새로 만든 스킬이 보이지 않으면 같은 실습 폴더에서 Claude Code를 종료한 뒤 다시 실행한다. `/reload-plugins`는 플러그인 변경을 반영할 때 사용하는 명령이다.

## 6. 기본 호출 실습

### 새 대화에서 직접 호출

스킬을 만들 때 나눈 대화를 비우고 새 대화에서 동작을 확인한다. Claude Code에서 실행한다.

```text
/clear
```

그다음 아래 요청을 입력한다.

```text
/prd-feature TODO 앱에 우선순위 태그 기능을 추가해줘. 아직 앱 코드는 없는 기획 연습이야. 높음/보통/낮음 선택, 기본값 보통, 우선순위 정렬을 포함하고 자동 추천과 화면 전체 디자인 변경은 제외해줘. PRD만 작성하고 구현하지 마.
```

- PRD에 여섯 항목이 모두 있는지 확인한다.
- 실제로 존재하지 않는 앱 파일이나 실행하지 않은 테스트 결과를 사실처럼 설명하지 않는지 확인한다.
- 코드를 작성하지 않고 사용자 승인을 기다리는지 확인한다.

### 선택 실습: 자동 호출 확인

직접 호출을 마쳤다면 스킬 이름 없이도 사용되는지 확인한다. `/clear`로 대화를 비운 뒤 아래 요청을 입력한다.

```text
TODO 앱에 우선순위 태그 기능을 추가해줘. 아직 코드가 없는 기획 연습이니 요구사항부터 정리하고 구현은 하지 마.
```

- Claude Code에 스킬 사용 표시가 나타나는지 확인하고, 작성된 PRD도 검토한다. PRD 형식의 답변이 나왔더라도 스킬이 사용되지 않았을 수 있다.
- 자동 호출 여부는 요청 내용과 `description`에 따라 달라질 수 있다. 호출되지 않으면 `/prd-feature`로 직접 호출한다.

## 7. 문제가 생기면 확인

| 문제 | 확인 순서 |
|---|---|
| `/plugin` 명령이 없음 | CLI 버전 확인 → 1회차 npm 설치 명령으로 업데이트 → 재시작 |
| skill-creator를 찾지 못함 | 공식 마켓플레이스 등록 → 설치 → `/plugin`의 활성화 상태 확인 |
| `/prd-feature`가 없음 | 실행 폴더 → `.claude/skills/prd-feature/SKILL.md` 경로 → frontmatter → 재시작 |
| 자동으로 호출되지 않음 | description의 조건 확인 → `/prd-feature`로 직접 호출 |
| 확인 없이 구현하려 함 | 실행 중단 → 스킬 본문에 사용자 승인 후 구현하도록 수정 요청 → `/clear` 후 다시 호출 |
| 평가 도구 실행을 제안함 | 스킬 파일 작성과 직접 호출만 진행한다고 답변 |

문제가 해결되지 않으면 실행한 명령과 오류 메시지를 강사에게 공유한다. 공유할 내용에 API 키나 토큰이 포함되지 않았는지 먼저 확인한다.

## 8. 명령 최종 확인

| 명령 | 실행 위치 | 용도 |
|---|---|---|
| `claude` | Git Bash | 대화형 실행 |
| `/status` | Claude Code | 로그인 상태 확인 |
| `/plugin` | Claude Code | 플러그인 설치·활성화 상태 확인 |
| `/plugin install skill-creator@claude-plugins-official` | Claude Code | 제작 도구 설치 |
| `/reload-plugins` | Claude Code | 플러그인 변경 반영 |
| `/skill-creator:skill-creator` | Claude Code | 스킬 제작 시작 |
| `/prd-feature 요청` | Claude Code | 만든 프로젝트 스킬 호출 |
| `/clear` | Claude Code | 현재 대화 맥락 비우기 |
| `/exit` | Claude Code | 종료 |

## 9. 마무리

- `SKILL.md`에 사용 조건과 PRD 작성 절차가 있는지 확인한다.
- 직접 호출한 결과에 PRD 여섯 항목이 있고, 구현 전에 승인을 기다리는지 확인한다.
- 공통 실습 폴더를 유지한다. 3회차에서는 같은 폴더에서 MCP를 연결한다.
- 4회차에서 다른 로컬 저장소 폴더를 사용하면 `.claude/skills/prd-feature` 폴더를 해당 저장소에도 복사한다.
- 질문과 답변을 진행한다.

공식 참고: [Skills](https://code.claude.com/docs/en/skills), [플러그인 설치](https://code.claude.com/docs/en/discover-plugins).