# GitHub MCP 연결하기 실습 진행 순서

## 1. 실습 환경 준비

- Windows + VS Code + Git Bash에서 진행한다.
- [1회차](../Claude_1회차_CLI_설치와_계정_연결하기/README.md)의 Claude Code 설치와 Pro 계정 연결을 완료한다.
- 수업 전에 GitHub에 로그인하고 **본인 소유의 연습용 저장소**를 준비한다. 업무 저장소는 사용하지 않는다.
- GitHub에서 New repository를 선택하고 저장소 이름을 `claude-code-practice`로 입력한다. Add README를 선택해 저장소를 생성하고 Issues 기능을 사용할 수 있는지도 확인한다. 이번 회차는 저장소 조회와 Issue 생성을 실습하므로 앱 코드는 필요 없다.
- 생성한 저장소를 로컬에 준비하는 방법은 아래 둘 중 하나를 선택한다. 두 방법 모두 이후 실습은 준비한 저장소 폴더에서 진행한다.

### 방법 A. GitHub 저장소를 내려받아 시작하기

GitHub 저장소 화면에서 **Code**를 선택해 HTTPS 주소를 복사한다. Git Bash에서 실행한다. `<저장소_URL>`은 복사한 주소로 바꾼다.

```bash
cd ~
git clone <저장소_URL>
cd claude-code-practice
code .
```

### 방법 B. 2회차의 로컬 폴더에 저장소 연결하기

[2회차](../Claude_2회차_skill-creator로_PRD_스킬_만들기/README.md)에서 만든 `claude-code-practice` 폴더를 계속 사용하려면, GitHub 저장소를 비어 있는 로컬 폴더에 연결한다. `<저장소_URL>`은 GitHub 저장소의 HTTPS 주소로 바꾼다.

```bash
cd ~/claude-code-practice
git init
git remote add origin <저장소_URL>
git pull origin main
code .
```

- `git pull origin main`에서 기본 브랜치를 찾을 수 없다는 오류가 나면 GitHub 저장소의 기본 브랜치 이름을 확인하고 `main` 대신 사용한다.
- 2회차에서 만든 `.claude` 폴더가 있다면 `git pull` 전에 유지할 파일이 있는지 확인한다. 새 저장소의 README와 같은 파일을 만들었다면 충돌이 날 수 있다.

준비한 저장소 폴더의 Git Bash에서 아래 명령을 실행한다.

```bash
claude --version
git --version
```

## 2. MCP와 설정 범위 이해하기

- **MCP(Model Context Protocol)**: Claude Code가 외부 도구나 데이터에 접근할 때 사용하는 연결 규격이다. GitHub MCP를 연결하면 대화로 저장소를 조회하거나 Issue 생성을 요청할 수 있다.
- 이번에는 GitHub 공식 원격 MCP 서버에 HTTP로 연결한다. 별도 서버나 Docker를 설치할 필요는 없다.
- Claude 로그인과 GitHub 인증은 별개다. Pro 로그인만으로 GitHub에 접근할 수는 없다.

MCP를 등록할 때는 설정이 적용될 범위를 선택한다. 이번 기본 실습에서는 `local`을 사용한다.

| 설정 범위 | 적용 대상 | 이번 수업 |
|---|---|---|
| `local` | 현재 프로젝트에서 나만 사용 | 기본 실습 |
| `project` | 현재 프로젝트의 설정 파일로 팀과 공유 | 참고 |
| `user` | 내 모든 프로젝트에서 사용 | 사용하지 않음 |

## 3. GitHub 토큰 준비

**PAT(Personal Access Token)** 는 GitHub API에 접근할 때 사용하는 인증 토큰이다. 접근할 저장소와 권한을 세부적으로 지정할 수 있는 **Fine-grained PAT**를 발급한다.

### Fine-grained PAT 발급

브라우저에서 [GitHub 토큰 설정](https://github.com/settings/personal-access-tokens)을 연다.

1. Generate new token을 선택한다.
2. Token name에 `claude-code-practice`를 입력한다.
3. Expiration은 실습 기간에 필요한 만큼 짧게 정한다.
4. Resource owner는 본인 계정을 선택한다.
5. Repository access에서 **Only select repositories**를 선택하고 연습용 저장소만 지정한다.
6. Repository permissions를 아래처럼 설정하고 토큰을 발급한다.

| 권한 | 3회차 설정 | 용도 |
|---|---|---|
| Metadata | Read-only, 기본 부여 | 저장소 정보 확인 |
| Contents | Read-only | 저장소 파일 읽기 |
| Issues | Read and write | 작업이나 요구사항을 기록하는 Issue 조회·생성 |
| Pull requests | Read-only | 코드 변경의 검토와 병합을 요청하는 PR 조회 |

- 토큰 권한은 본인 계정의 권한을 넘을 수 없다.
- 조직 저장소는 관리자 승인이나 정책에 따라 접근이 제한될 수 있으므로 이번에는 본인 소유 저장소를 사용한다.

### 현재 터미널에 토큰 입력

Git Bash에서 아래 명령을 **한 줄씩** 실행한다. 첫 명령의 입력 대기 상태에서 토큰을 붙여넣고 Enter를 누른다. 입력값은 화면에 표시되지 않는다.

```bash
read -r -s -p "GitHub PAT: " GITHUB_PAT
echo "$GITHUB_PAT"
export GITHUB_PAT
```

- 토큰을 Claude 대화, README, 화면 캡처에 붙여넣지 않는다.
- 위 방법으로 입력하면 토큰 값이 명령 기록에 직접 남지 않는다. 다만 현재 Git Bash와 여기서 실행한 프로그램에는 환경변수로 전달되므로 환경변수 출력도 공유하지 않는다.
- 현재 Git Bash를 닫으면 환경변수 설정이 사라진다. 새 터미널에서는 토큰을 다시 입력한다.

## 4. GitHub MCP 등록

Claude Code가 열려 있다면 `/exit`로 종료한다. **토큰을 입력한 같은 Git Bash**에서 실행한다.

```bash
claude mcp add --transport http --scope local github https://api.githubcopilot.com/mcp/ --header 'Authorization: Bearer ${GITHUB_PAT}'
```

- 명령의 작은따옴표를 그대로 사용한다. `${GITHUB_PAT}`를 실제 토큰으로 바꾸지 않는다. 설정에는 환경변수 이름을 저장하고, 연결할 때 해당 변수의 토큰 값을 사용한다.
- 등록 성공 메시지는 설정 저장을 의미한다. 실제 인증 성공은 다음 단계에서 확인한다.
- 이미 `github`가 있다면 기존 설정을 먼저 확인하고, 다른 실습이나 업무 설정을 임의로 삭제하지 않는다.

### 참고: 팀과 설정 공유하기

기본 실습에서는 위의 `local` 설정만 사용한다. 팀과 설정을 공유할 때는 다음과 같이 `project` 범위를 사용할 수 있다. 지금은 실행하지 않고 차이만 확인한다.

```bash
claude mcp add --transport http --scope project github https://api.githubcopilot.com/mcp/ --header 'Authorization: Bearer ${GITHUB_PAT}'
```

- 프로젝트 루트의 `.mcp.json`에 설정이 저장된다. 공유 전 실제 토큰이 아닌 환경변수 참조만 들어 있는지 확인한다.
- 팀원은 각자 토큰을 설정하고 최초 실행 시 서버 사용을 승인한다.
- 같은 이름의 `local` 설정이 있으면 `project` 설정보다 우선한다. `project` 범위로 전환할 때는 기존 설정이 본인의 실습용 설정인지 확인한 뒤 7단계의 제거 명령을 사용한다.

## 5. 연결 상태 확인

Git Bash에서 실행한다.

```bash
claude mcp list
claude mcp get github
claude
```

Claude Code에서 실행한다.

```text
/mcp
```

- `github`의 연결 상태와 사용 가능한 도구를 확인한다.
- 승인 대기라면 등록한 서버 주소를 확인하고 승인한다.
- 캐시된 상태, 즉 이전 연결 정보가 표시되면 서버 메뉴에서 재연결하거나 6단계의 저장소 조회를 실행해 현재 연결을 확인한다.
- 기존 설정에 토큰이 직접 저장되어 있을 수 있으므로 설정 출력은 공유·녹화 전에 확인한다.

## 6. GitHub 작업 요청하기

### 저장소 읽기

Claude Code에 입력한다.

```text
GitHub MCP를 사용해서 현재 프로젝트 저장소의 기본 브랜치와 루트 파일 목록을 확인해줘. 파일이나 Issue는 수정하지 마. MCP로 조회할 수 없으면 다른 도구로 대신 진행하지 말고 이유를 알려줘.
```

응답에 나온 기본 브랜치와 파일 목록을 GitHub 화면과 비교한다. 연결 상태가 정상으로 표시되더라도 실제 저장소 조회가 성공했는지 확인한다.

### Issue 초안 확인 후 생성

```text
현재 프로젝트 저장소에 "[실습] GitHub MCP 연결 확인"이라는 Issue를 만들고 싶어. 본문에는 저장소 조회 성공 여부와 다음 회차에 TODO 우선순위 기능을 검토한다는 내용을 넣어줘. 같은 제목의 Issue가 있으면 먼저 알려줘. 아직 생성하지 말고 제목과 본문만 보여줘.
```

대상 저장소와 제목, 본문을 확인한다. 같은 제목의 Issue가 없다면 아래 메시지를 입력해 생성을 승인한다. 이미 있다면 기존 Issue를 확인하고 중복 생성하지 않는다.

```text
확인했어. 방금 확인한 저장소에 그 내용으로 Issue를 하나만 생성해줘. 생성된 번호와 URL을 알려줘.
```

- 권한 승인 창이 나오면 해당 저장소에 Issue를 만드는 요청인지 확인한다.
- 브라우저에서 URL을 열어 실제 생성 결과를 확인한다.

### 선택 실습: PR 조회

Issue 생성을 마쳤다면 열린 PR 목록도 조회한다.

```text
GitHub MCP로 현재 프로젝트의 열린 PR 목록을 보여줘. 없다면 없다고만 알려줘. 새 PR은 만들지 마.
```

열린 PR이 있다면 해당 PR의 URL을 전달하고 변경 내용과 주의할 점을 요약해 달라고 요청한다. 열린 PR이 없다면 조회 결과만 확인하고 마친다.

## 7. 문제가 생기면 확인

| 문제 | 확인 순서 |
|---|---|
| 등록됐지만 인증 실패 | 같은 터미널의 토큰 입력 여부 → 만료·취소 여부 → 재연결 |
| 저장소 조회가 안 됨 | `OWNER/REPO` → 선택한 저장소 → Contents 읽기 권한 → 조직 승인 |
| Issue 생성이 안 됨 | Issues 기능 활성화 → Issues 쓰기 권한 → 본인 계정의 접근 권한 |
| MCP가 안 보임 | 등록한 폴더에서 실행했는지 → `claude mcp list` → 재시작 |
| 동일한 이름이 이미 있음 | `claude mcp get github`로 범위 확인 → 본인 실습 설정만 제거·재등록 |
| 기관 정책이나 네트워크로 접속이 차단됨 | 오류 메시지 확인 → 강사에게 문의, 정책을 우회하지 않음 |

잘못 등록한 **본인 실습용 local 설정만** 제거할 때 Git Bash에서 실행한다.

```bash
claude mcp remove --scope local github
```

제거 후에는 4단계의 기본 등록 명령을 다시 실행한다. 토큰 값만 변경했다면 설정을 삭제할 필요 없이 토큰을 입력한 Git Bash에서 Claude Code를 다시 실행한다.

문제가 해결되지 않으면 실행한 명령과 오류 메시지를 강사에게 공유한다. 토큰 값은 공유하지 않는다.

## 8. 명령 최종 확인

| 명령 | 실행 위치 | 용도 |
|---|---|---|
| `read -r -s -p "GitHub PAT: " GITHUB_PAT` | Git Bash | 화면에 표시하지 않고 토큰 입력 |
| `export GITHUB_PAT` | Git Bash | Claude Code에 환경변수 전달 |
| `claude mcp add ...` | Git Bash | MCP 서버 등록 |
| `claude mcp list` | Git Bash | 서버 목록·상태 확인 |
| `claude mcp get github` | Git Bash | GitHub 설정·상태 확인 |
| `/mcp` | Claude Code | 연결 상태·도구 확인 |
| `claude mcp remove --scope local github` | Git Bash | 실습용 local 설정 제거 |
| `/exit` | Claude Code | 종료 |

`read -r -s -p "GitHub PAT: " GITHUB_PAT` 명령의 옵션은 다음과 같다.

| 옵션 | 의미 |
|---|---|
| `-r` | 입력값의 백슬래시(`\`)를 이스케이프 문자로 해석하지 않고 그대로 저장한다. |
| `-s` | 입력값을 화면에 표시하지 않는다(silent mode). 비밀번호나 토큰 입력에 사용한다. |
| `-p "GitHub PAT: "` | 입력을 기다리며 지정한 문구를 프롬프트로 보여준다. |

## 9. 마무리

- 저장소 조회 결과와 생성한 Issue의 번호·URL을 확인한다.
- GitHub에서 읽은 Issue나 파일에 토큰 공개 또는 실습과 관계없는 명령 실행을 요구하는 내용이 있으면 따르지 않는다.
- 4회차에서 같은 폴더를 사용하면 `local` MCP 설정을 이어서 사용할 수 있다. 새 터미널에서는 토큰을 다시 입력한다.
- 더 이상 사용하지 않는 토큰은 GitHub 설정에서 삭제한다. 다음 회차에도 사용할 토큰은 비밀번호 관리자 등 안전한 곳에 보관하고 유효기간을 확인한다.
- 이번 Git Bash에서 입력한 토큰 환경변수를 지우려면 아래 명령을 실행한다. 이 명령은 현재 터미널의 `GITHUB_PAT` 값만 지우며, GitHub에서 발급한 토큰을 폐기하지는 않는다.

```bash
unset GITHUB_PAT
```

- 질문과 답변을 진행한다.

공식 참고: [Claude Code MCP](https://code.claude.com/docs/en/mcp), [GitHub 서버 연결 안내](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md), [PAT 관리](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).