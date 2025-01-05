import sounddevice as sd
import wave
import config
import google.generativeai as genai

# 録音設定
RATE = 44100
CHANNELS = 1
DURATION = 5
OUTPUT_FILENAME = "record.wav"

# print("録音中...")

# 録音処理
# recording = sd.rec(int(DURATION * RATE), samplerate=RATE, channels=CHANNELS, dtype="int16")
# sd.wait()

# print("録音終了")

# WAVファイルに保存
# with wave.open(OUTPUT_FILENAME, "wb") as wf:
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(2)
#     wf.setframerate(RATE)
#     wf.writeframes(recording.tobytes())
# print(f"{OUTPUT_FILENAME}に保存されました。")


# AIモデル
genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
response = model.generate_content("こんにちは")
print(response.text)