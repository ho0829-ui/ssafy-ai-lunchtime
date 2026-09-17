# Claude Code CLI 실습 진행 순서

## 1. 실습 환경 준비

- VS Code에서 작업할 폴더를 연다.
- 터미널 기본 프로필을 **Git Bash**로 선택한다.
- [Node.js 공식 사이트](https://nodejs.org/)에서 **LTS 버전**을 설치한다.
- Pro 계정 또는 사용할 API 키를 준비한다.

Git Bash를 새로 열고 Node.js와 npm이 준비되었는지 확인한다.

```bash
node --version
npm --version
```

- Node.js는 **LTS 버전**을 사용한다.
- 명령어를 찾지 못하면 Node.js 설치 후 VS Code와 Git Bash를 다시 연다.

## 2. 설치 및 버전 확인

Git Bash에서 실행한다.

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

- npm 권한 오류가 나면 관리자 권한으로 Git Bash를 실행하지 말고, Node.js LTS를 기본 설정으로 다시 설치한 뒤 새 Git Bash에서 다시 시도한다.
- 이미 설치했다면 버전만 확인한다.

## 3. 계정 연결

아래 방법 중 **하나만 선택**한다. 현재 수업은 Pro 계정을 사용한다.

### 방법 A. Pro 계정

```bash
claude
```

1. 구독 계정 로그인을 선택한다.
2. 브라우저에서 Pro 계정으로 인증한다.
3. VS Code 터미널로 돌아온다.

### 방법 B. Claude API 키

Claude Console에서 API 키를 발급받은 후 Git Bash에서 실행한다.

```bash
unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN
export ANTHROPIC_API_KEY="본인의_Claude_API_키"
```

> Git Bash를 닫으면 이 설정은 사라진다.

### 방법 C. SSAFY GMS

현재 수업에서는 실행하지 않고 설정 방식만 확인한다.

```bash
unset ANTHROPIC_AUTH_TOKEN​
export ANTHROPIC_BASE_URL="https://gms.ssafy.io/gmsapi/api.anthropic.com"​
export ANTHROPIC_API_KEY="본인의_GMS_키"​
export ANTHROPIC_MODEL="claude-opus-4"​
```

## 4. API·GMS에서 Pro로 전환

Claude Code에서 종료한다.

```text
/exit
```

Git Bash에서 실행한다.

```bash
unset ANTHROPIC_API_KEY
unset ANTHROPIC_BASE_URL
unset ANTHROPIC_AUTH_TOKEN
claude
```

Claude Code에서 실행한다.

```text
/login
```

Pro 계정을 선택한다.

## 5. 연결 상태 확인

Claude Code에서 실행한다.

```text
/status
```

종료 후 Git Bash에서 실제 응답을 확인한다.

```bash
claude -p "안녕, 한 문장으로 인사해줘"
```

## 6. 기본 명령 실습

### 대화형으로 실행

Git Bash에서 실행한다.

```bash
claude
```

### 한 번만 요청하고 종료

```bash
claude -p "안녕, 한 문장으로 인사해줘"
```

### 도움말과 상태 확인

Claude Code 안에서 실행한다.

```text
/help
/status
```

### 자주 쓰는 세션 명령

Claude Code 안에서 실행한다.

```text
/clear
/compact
/model
/init
/exit
```

- `/clear`: 현재 대화 맥락을 비운다.
- `/compact`: 이전 대화 내용을 요약해 컨텍스트 사용량을 줄인다. 긴 작업을 계속할 때 사용한다.
- `/model`: 현재 세션에서 사용할 모델을 확인하거나 변경한다.
- `/init`: 현재 프로젝트를 분석해 `CLAUDE.md` 기본 안내 파일을 만든다. 프로젝트 작업을 시작할 때 한 번 실행한다.
- `/exit`: Claude Code를 종료한다.
- `/clear`는 프로젝트 파일이나 수정한 코드를 되돌리지 않는다.

### 이전 작업 이어가기

Git Bash에서 실행한다.

```bash
claude --resume
```

- 이전 대화 목록에서 하나를 골라 이어서 작업한다.

## 7. 문제가 생기면 확인

| 문제 | 확인 순서 |
|---|---|
| CLI를 찾지 못함 | VS Code 재실행 → Git Bash 실행 → `claude --version` |
| Pro 로그인 문제 | 기존 키·주소 설정 확인 → `/login` |
| API 키 인증 문제 | 키 → 계정 권한 → API 사용 가능 상태 |
| GMS 접속 문제 | 제공 주소 → GMS 키 → 이용 가능 시점 |

## 8. 명령 최종 확인

| 명령 | 용도 |
|---|---|
| `claude` | 대화형 실행 |
| `claude -p "요청"` | 한 번 요청하고 종료 |
| `/help` | 명령 목록 확인 |
| `/status` | 현재 연결 상태 확인 |
| `/clear` | 대화 맥락 비우기 |
| `/compact` | 긴 대화를 요약해 컨텍스트 사용량 줄이기 |
| `/model` | 사용할 모델 확인 또는 변경 |
| `/init` | 프로젝트용 `CLAUDE.md` 기본 파일 만들기 |
| `/exit` | Claude Code 종료 |
| `/login` | 로그인 계정 변경 |
| `claude --resume` | 이전 대화를 선택해 이어서 작업 |

## 9. 마무리

- 설치 여부를 확인한다.
- 선택한 방식으로 연결되었는지 확인한다.
- 기본 명령을 한 번씩 실행한다.
- 질문과 답변을 진행한다.