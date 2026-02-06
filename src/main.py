#!/usr/bin/env python3
"""
Project Shoulder - Debug Version
"""

import os
import sys
import base64
import subprocess
from datetime import datetime

print("[DEBUG] 모듈 로딩 시작...")

try:
    from google import genai
    from google.genai import types
    print("[DEBUG] google.genai 로드 성공")
except ImportError as e:
    print(f"[ERROR] google.genai 로드 실패: {e}")
    sys.exit(1)

try:
    from pynput import keyboard
    print("[DEBUG] pynput 로드 성공")
except ImportError as e:
    print(f"[ERROR] pynput 로드 실패: {e}")
    sys.exit(1)

try:
    from mss import mss
    print("[DEBUG] mss 로드 성공")
except ImportError as e:
    print(f"[ERROR] mss 로드 실패: {e}")
    sys.exit(1)


class ScreenCoach:
    SYSTEM_PROMPT = """당신은 '숄더'입니다. 화면을 보고 3문장으로 가이드해주세요."""

    def __init__(self):
        print("[DEBUG] ScreenCoach 초기화 시작")
        
        api_key = os.getenv('GOOGLE_GENERATIVE_AI_API_KEY')
        if not api_key:
            print("[ERROR] API 키가 없습니다!")
            sys.exit(1)
        
        if api_key == "너의_API_키" or len(api_key) < 20:
            print("[ERROR] 유효하지 않은 API 키입니다! 실제 Gemini API 키를 입력하세요.")
            sys.exit(1)
            
        print(f"[DEBUG] API 키 확인 (앞 10자): {api_key[:10]}...")
        
        try:
            self.client = genai.Client(api_key=api_key)
            print("[DEBUG] Gemini 클라이언트 초기화 성공")
        except Exception as e:
            print(f"[ERROR] Gemini 초기화 실패: {e}")
            sys.exit(1)
        
        self.sct = mss()
        self.processing = False
        print("[DEBUG] 초기화 완료")

    def capture_screen(self):
        print("[DEBUG] 화면 캡처 시작")
        try:
            screenshot = self.sct.shot()
            print(f"[DEBUG] 스크린샷 저장: {screenshot}")
            with open(screenshot, "rb") as f:
                data = base64.b64encode(f.read()).decode('utf-8')
                print(f"[DEBUG] Base64 변환 완료 (길이: {len(data)})")
                return data
        except Exception as e:
            print(f"[ERROR] 캡처 실패: {e}")
            return None

    def analyze_screen(self, image_base64):
        print("[DEBUG] AI 분석 시작")
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(self.SYSTEM_PROMPT),
                            types.Part.from_text("이 화면을 분석해주세요."),
                            types.Part.from_bytes(
                                data=base64.b64decode(image_base64),
                                mime_type="image/png"
                            )
                        ]
                    )
                ]
            )
            print("[DEBUG] AI 응답 수신 완료")
            return response.text
        except Exception as e:
            print(f"[ERROR] AI 분석 실패: {e}")
            return f"오류: {e}"

    def speak(self, msg):
        print(f"[DEBUG] TTS 시작: {msg[:50]}...")
        try:
            subprocess.run(['say', '-v', 'Yuna', msg], check=True)
            print("[DEBUG] TTS 완료")
        except Exception as e:
            print(f"[ERROR] TTS 실패: {e}")

    def on_analyze(self):
        print("\n" + "="*50)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 핫키 감지됨!")
        print("="*50)
        
        if self.processing:
            print("[WARN] 이미 처리 중...")
            return
        
        self.processing = True
        
        img = self.capture_screen()
        if not img:
            self.processing = False
            return
            
        result = self.analyze_screen(img)
        
        print("\n🎯 가이드:")
        print("-"*40)
        print(result)
        print("-"*40 + "\n")
        
        self.speak(result)
        self.processing = False

    def run(self):
        print("\n" + "="*50)
        print("🎯 Project Shoulder (Debug Mode)")
        print("="*50)
        print("Ctrl+Shift+S: 분석 | Ctrl+Shift+Q: 종료")
        print("="*50)
        print("\n[DEBUG] 핫키 리스너 시작...")
        
        # 핫키 등록 확인
        hotkeys = {
            '<ctrl>+<shift>+s': self.on_analyze,
            '<ctrl>+<shift>+q': lambda: (print("[DEBUG] 종료 요청"), False)
        }
        print(f"[DEBUG] 등록된 핫키: {list(hotkeys.keys())}")
        
        try:
            with keyboard.GlobalHotKeys(hotkeys) as h:
                print("[DEBUG] GlobalHotKeys 시작 성공")
                print("[INFO] 대기 중... Ctrl+Shift+S를 누르세요")
                h.join()
        except Exception as e:
            print(f"[ERROR] 핫키 리스너 에러: {e}")
            print("[TIP] 손쉬운 사용 권한을 확인하세요!")


if __name__ == "__main__":
    print("[DEBUG] 프로그램 시작")
    try:
        coach = ScreenCoach()
        coach.run()
    except KeyboardInterrupt:
        print("\n[INFO] 종료됨")
    except Exception as e:
        print(f"[FATAL] {e}")
