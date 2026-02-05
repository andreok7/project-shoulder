# 🍎 Mac 설치 가이드

## 1단계: 프로젝트 다운로드

서버에서 Mac으로 파일 복사:
```bash
# Mac 터미널에서 실행
mkdir -p ~/Projects/project-shoulder
cd ~/Projects/project-shoulder

# 서버에서 파일 가져오기 (scp 사용)
# 또는 아래 코드를 직접 복사해서 파일 생성
```

## 2단계: Python 환경 설정

```bash
# Python 3.11+ 확인
python3 --version

# 가상환경 생성 (권장)
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install mss pynput google-generativeai Pillow
```

## 3단계: API 키 설정

```bash
# .env 파일 생성 또는 직접 export
export GOOGLE_GENERATIVE_AI_API_KEY="your-api-key-here"

# 영구 설정 (zshrc에 추가)
echo 'export GOOGLE_GENERATIVE_AI_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

## 4단계: 권한 설정 (중요!)

Mac에서 화면 캡처와 키보드 감지를 위해 권한이 필요합니다:

1. **시스템 환경설정** → **개인정보 보호 및 보안**
2. **화면 기록** → Python/터미널 앱 허용
3. **손쉬운 사용** → Python/터미널 앱 허용 (핫키용)

## 5단계: 실행

```bash
cd ~/Projects/project-shoulder
source venv/bin/activate
python src/main.py
```

## 사용법

| 단축키 | 기능 |
|--------|------|
| `Cmd + Shift + S` | 화면 캡처 + AI 분석 |
| `Cmd + Shift + Q` | 종료 |

## 문제 해결

### "권한이 없습니다" 오류
→ 시스템 환경설정에서 터미널/Python에 화면 기록 권한 부여

### TTS가 작동하지 않음
→ Mac에 한국어 음성(Yuna) 설치 확인
→ `say -v ?` 로 사용 가능한 음성 확인

### API 오류
→ GOOGLE_GENERATIVE_AI_API_KEY 환경변수 확인
