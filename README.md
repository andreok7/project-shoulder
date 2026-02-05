# Project Shoulder 🎯

> 어깨 너머로 화면을 보며 실시간 가이드해주는 AI 코치

## 컨셉: The Lazy Observer
- 평소엔 조용히 대기
- 사용자가 요청할 때만 활성화
- 비용 최소화 + 프라이버시 보호

## Quick Start (Mac)

### 1. 설치
```bash
cd project-shoulder
pip install -r requirements.txt
```

### 2. API 키 설정
```bash
export GOOGLE_GENERATIVE_AI_API_KEY="your-api-key"
```

### 3. 실행
```bash
python src/main.py
```

### 4. 사용법
- `Cmd + Shift + S`: 화면 캡처 + AI 분석
- `Cmd + Shift + Q`: 종료

## 기술 스택
- Python 3.11+
- mss (화면 캡처)
- pynput (핫키)
- Gemini 2.0 Flash (Vision)
- macOS say (TTS)

## 팀
- Andrew: Product Owner
- 앤디: Development
- 알티: Design & Prompt

---
*Toonit AI Team - 2026*
