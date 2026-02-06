#!/usr/bin/env python3
"""
Project Shoulder - Simple Version (Enter key to analyze)
"""

import os
import sys
import base64
import subprocess

print("[DEBUG] 모듈 로딩...")

from google import genai
from google.genai import types
from mss import mss

print("[DEBUG] 로드 완료")


class ScreenCoach:
    SYSTEM_PROMPT = """당신은 '숄더'입니다. 화면을 보고 한국어로 3문장 이내로 가이드해주세요."""

    def __init__(self):
        api_key = os.getenv('GOOGLE_GENERATIVE_AI_API_KEY')
        if not api_key or len(api_key) < 20:
            print("❌ API 키가 없거나 유효하지 않습니다!")
            sys.exit(1)
        
        print(f"[DEBUG] API 키 확인됨: {api_key[:10]}...")
        self.client = genai.Client(api_key=api_key)
        self.sct = mss()
        print("[DEBUG] 초기화 완료")

    def capture_screen(self):
        print("📸 화면 캡처 중...")
        screenshot = self.sct.shot()
        with open(screenshot, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def analyze_screen(self, image_base64):
        print("🧠 AI 분석 중...")
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(self.SYSTEM_PROMPT),
                            types.Part.from_text("이 화면을 분석하고 다음 단계를 안내해주세요."),
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

    def run(self):
        print("\n" + "="*50)
        print("🎯 Project Shoulder")
        print("="*50)
        print("Enter: 화면 분석 | q + Enter: 종료")
        print("="*50 + "\n")
        
        while True:
            try:
                user_input = input("▶ Enter를 눌러 화면 분석... ")
                
                if user_input.lower() == 'q':
                    print("👋 종료합니다")
                    break
                
                # 화면 캡처 & 분석
                img = self.capture_screen()
                result = self.analyze_screen(img)
                
                print("\n" + "─"*40)
                print("🎯 가이드:")
                print(result)
                print("─"*40 + "\n")
                
                self.speak(result)
                
            except KeyboardInterrupt:
                print("\n👋 종료합니다")
                break


if __name__ == "__main__":
    ScreenCoach().run()
