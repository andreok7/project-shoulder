#!/usr/bin/env python3
"""
Project Shoulder - The Lazy Observer
어깨 너머로 화면을 보며 가이드해주는 AI 코치

By: Toonit A-Team
"""

import os
import base64
import subprocess
from datetime import datetime

from google import genai
from google.genai import types
from pynput import keyboard
from mss import mss


class ScreenCoach:
    SYSTEM_PROMPT = """당신은 '숄더'입니다. 사용자의 어깨 너머로 화면을 보며 도움을 주는 AI 코치입니다.
- 한국어로 3문장 이내 답변
- 다음 단계를 명확히 안내
- 버튼/메뉴 위치 구체적으로 설명"""

    def __init__(self):
        api_key = os.getenv('GOOGLE_GENERATIVE_AI_API_KEY')
        if not api_key:
            raise ValueError("❌ GOOGLE_GENERATIVE_AI_API_KEY 환경변수 필요")
        
        self.client = genai.Client(api_key=api_key)
        self.sct = mss()
        self.processing = False
        
        print("=" * 50)
        print("🎯 Project Shoulder")
        print("=" * 50)
        print("Cmd+Shift+S: 분석 | Cmd+Shift+Q: 종료")
        print("=" * 50)

    def capture_screen(self):
        screenshot = self.sct.shot()
        with open(screenshot, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def analyze_screen(self, image_base64):
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(self.SYSTEM_PROMPT),
                            types.Part.from_text("이 화면을 분석하고 가이드해주세요."),
                            types.Part.from_bytes(
                                data=base64.b64decode(image_base64),
                                mime_type="image/png"
                            )
                        ]
                    )
                ]
            )
            return response.text
        except Exception as e:
            return f"❌ 오류: {e}"

    def speak(self, msg):
        subprocess.run(['say', '-v', 'Yuna', msg])

    def on_analyze(self):
        if self.processing:
            return
        self.processing = True
        print(f"\n📸 [{datetime.now().strftime('%H:%M:%S')}] 캡처 중...")
        
        img = self.capture_screen()
        print("🧠 분석 중...")
        result = self.analyze_screen(img)
        
        print(f"\n🎯 가이드:\n{result}\n")
        self.speak(result)
        self.processing = False

    def run(self):
        with keyboard.GlobalHotKeys({
            '<cmd>+<shift>+s': self.on_analyze,
            '<cmd>+<shift>+q': lambda: False
        }) as h:
            h.join()


if __name__ == "__main__":
    ScreenCoach().run()
