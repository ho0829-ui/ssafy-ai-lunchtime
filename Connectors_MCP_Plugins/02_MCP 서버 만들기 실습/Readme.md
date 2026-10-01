# 프로젝트 초기 세팅

### uv 설치 (설치 후 터미널 재실행 필요)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### mcp 서버 기본 세팅
```bash
uv init weather
cd weather

uv venv
source .venv/bin/activate

uv add "mcp[cli]"

touch weather.py
```

## Local 파일 기반 
### 1. mcp 서버 실행을 위한 uv 경로 찾기
```bash
cygpath -m "$(which uv)"
```

### 2. 현재 mcp 서버 경로 찾기(mcp 서버 코드가 존재하는 터미널에서 실행할 것 )
```bash
cygpath -m "$(pwd)"
```

### claude_desktop_config.json 에 입력할 코드 (command 와 args에 있는 경로는 위를 참고해서 작성할 것 )
```json
  "mcpServers": {
    "weather": {
      "command": "1번 명령어를 입력해서 나온 uv 경로를 입력",
      "args": [
        "--directory",
        "2번 명령어를 입력해서 나온 mcp server 경로를 입력",
        "run",
        "weather.py"
      ]
    }
  },

```
### claude_desktop_config.json 샘플 코드 
```json
  "mcpServers": {
    "weather": {
      "command": "C:/Users/SSAFY/.local/bin/uv.exe",
      "args": [
        "--directory",
        "C:/Users/SSAFY/Desktop/AI Lunch Time/교재/mcp_server_codes/weather",
        "run",
        "weather.py"
      ]
    }
  },
```

### mcp 서버 활용하는 지 확인하기 위한 질문 
```prompt
what weather alerts are active for NY
```

## Github 배포 기반 MCP 서버 배포 
### 깃허브에 코드 업로드 
```bash
# 1. Stage에 파일 추가 
git add .

# 2. 커밋 작성
git commit –m “Init Commit:MCP Server”

# 3. 저장소 연결
git remote add origin [git 주소]

# 4. 저장소에 코드 업로드
git push origin [master(혹은 main)]
```

### 깃허브에 업로드된 저장소를 기반으로 한 mcp 호출을 위한 claude_desktop_config.json 파일에 작성할 코드 
(git+ 뒤에 중괄호는 지워야함)
(git+ 밑에 있는 것은 mcp 서버 폴더명과 맞춰야 함 )
```json
    "weather-github": {
      "command": "C:/Users/SSAFY/.local/bin/uvx.exe",
      "args": [
        "--from",
        "git+{https://github.com/jayden/jayden-mcp-weather.git}",
        "weather"
      ]
    }
```