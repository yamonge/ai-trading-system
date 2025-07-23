# 🚀 AI Trading System - 다른 컴퓨터 설정 가이드

## 📋 새 컴퓨터에서 설정하는 방법

### 1단계: 기본 설치
```bash
# Git 설치 확인
git --version

# Node.js 설치 확인  
node --version

# Python 설치 확인
python --version
```

### 2단계: 프로젝트 복제
```bash
git clone https://github.com/yamonge/ai-trading-system.git
cd ai-trading-system
```

### 3단계: VS Code 확장프로그램 자동 설치
VS Code에서 프로젝트 열면 자동으로 추천 확장프로그램 설치 제안이 나타납니다.

또는 수동 설치:
```bash
# 필수 확장프로그램들
code --install-extension ms-python.python
code --install-extension ms-python.pylance  
code --install-extension github.copilot
code --install-extension github.copilot-chat
code --install-extension visualstudioexptteam.vscodeintellicode
code --install-extension codeium.codeium
code --install-extension christian-kohler.path-intellisense
code --install-extension gruntfuggly.todo-tree
code --install-extension alefragnani.project-manager
code --install-extension xyz.local-history
code --install-extension nguyenngoclong.terminal-keeper
code --install-extension bradlc.vscode-tailwindcss
code --install-extension ms-python.black-formatter
code --install-extension ms-python.isort
```

### 4단계: Python 환경 설정
```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화 (Windows)
.venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)  
source .venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 5단계: AI 어시스턴트 활성화
새 채팅에서 다음 명령어 실행:
```
프로젝트 컨텍스트 로드해줘
```

## 🎯 자동화 스크립트

### Windows PowerShell
```powershell
# setup.ps1
git clone https://github.com/yamonge/ai-trading-system.git
cd ai-trading-system
python -m venv .venv
.venv\Scripts\activate  
pip install -r requirements.txt
code .
```

### Mac/Linux Bash
```bash
#!/bin/bash
# setup.sh
git clone https://github.com/yamonge/ai-trading-system.git
cd ai-trading-system
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
code .
```

## 💡 팁
- VS Code Settings Sync를 활성화하면 확장프로그램과 설정이 자동 동기화됩니다
- GitHub Copilot 로그인은 각 기기에서 한 번씩 필요합니다
- 모든 프로젝트 메모리와 설정은 Git에 저장되어 있어 자동으로 복원됩니다

## 🚨 주의사항
- API 키가 필요한 서비스들은 각 기기에서 재설정 필요
- Codeium 로그인은 선택사항 (로그인 없이도 작동)
- 첫 실행 시 Python 인터프리터 선택 필요

---
*이 가이드만 따라하면 어떤 컴퓨터에서도 동일한 AI 개발 환경을 구축할 수 있습니다!*
