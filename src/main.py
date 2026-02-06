#!/usr/bin/env python3
"""
Project Shoulder - Fixed Version
"""

import os
import sys
import base64
import subprocess

print("[DEBUG] 모듈 로딩...")

import google.generativeai as genai
from mss import mss
from PIL import Image

print("[DEBUG] 로드 완료")


class ScreenCoach:
    def __init__(self):
        api_key = os.getenv('GOOGLE_GENERATIVE_AI_API_KEY')
        if not api_key or len(api_key) < 20:
            print("❌ API 키가 없거나 유효하지 않습니다!")
            sys.exit(1)
        
        print(f"[DEBUG] API 키 확인됨: {api_key[:10]}...")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.sct = mss()
        print("[DEBUG] 초기화 완료")

    def capture_screen(self):
        print("📸 화면 캡처 중...")
        monitor = self.sct.monitors[1]
        sct_img = self.sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img

    def analyze_screen(self, img):
        print("🧠 AI 분석 중...")
        try:
            response = self.model.generate_content([
                "이 화면을 보고 사용자가 무엇을 하려는지 파악하고, 다음 단계를 한국어로 3문장 이내로 안내해줘.",
                img
            ])
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
