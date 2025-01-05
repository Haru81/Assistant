from dotenv import load_dotenv
import os

# APIキー設定
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
