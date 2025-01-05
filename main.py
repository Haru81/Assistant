import config
import sounddevice as sd
import google.generativeai as genai
import input_voice
import output_voice

response = ""

def connect_ai():
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
    response = model.generate_content("こんにちは、自己紹介してみて")
    print(response.text)

def output(text):
# 音声出力
    adapter = output_voice.Sbv2Adapter()
    data, sample_rate = adapter.get_voice(text)
    sd.play(data, sample_rate)
    sd.wait()

connect_ai()
# output(response.text)