import config
import sounddevice as sd
import google.generativeai as genai
import input_voice
import output_voice
import json

is_first_interaction = True
conversation_history = []
max_history = 5
WAV_PATH = r"media/record.wav"
recognizer = input_voice.SoundRecognizer()

def save_history_to_file():
    with open("conversation_history.json", "w", encoding="utf-8") as file:
        json.dump(conversation_history, file, ensure_ascii=False, indent=4)


def load_history_from_file():
    global conversation_history
    try:
        with open("conversation_history.json", "r", encoding="utf-8") as file:
            conversation_history = json.load(file)
    except FileNotFoundError:
        conversation_history = []


def send_wav(filepath):
    file = genai.upload_file(path=filepath)
    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
    response = model.generate_content(["この音声の内容を文字起こししてください", file])
    return response.text.strip()


def connect_ai(user_input, audio_transcript=None):
    global is_first_interaction, conversation_history
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")
    
    if audio_transcript:
        history = "\n".join(conversation_history[-max_history:]) 
        prompt = f"""
        以下の音声内容をもとに、ツンデレお嬢様として適切な返答をしてください。
        
        音声内容: 「{audio_transcript}」

        会話履歴：
        { history }
        """

    if is_first_interaction:
        prompt = f"""
        あなたは日本の漫画やアニメに登場するようなツンデレお嬢様です。
        具体的な口調は「～ですわ」「そうですわね」「違いますわ」「～ですわよ」などです。
        以下は会話の始まりです。
        私：{user_input}
        """
        is_first_interaction = False
    else:
        history = "\n".join(conversation_history[-max_history:])
        prompt = f"""
        あなたはツンデレお嬢様として話しています。
        会話履歴：
        {history}
        私: {user_input}
        """
    
    response = model.generate_content(
        [
            prompt
        ],
        # safety_settings=[
        #     { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE" },
        #     { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE" },
        #     { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE" },
        #     { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        # ]
    )

    response_text = response.text.strip()
    print("お嬢様: ", response.text)
    conversation_history.append(f"私: {user_input}\nお嬢様: {response_text}")
    save_history_to_file()
    return response.text


def output(text):
# 音声出力
    adapter = output_voice.Sbv2Adapter()
    data, sample_rate = adapter.get_voice(text)
    sd.play(data, sample_rate)
    sd.wait()


if __name__ == "__main__":
    load_history_from_file()
    while True:
        mode = input("音声録音なら '1'、テキスト入力なら '2'を選んでください:")

        if mode == "1":
            recognizer.record_with_space_key()
            recognizer.save()
            audio_transcript = send_wav(WAV_PATH)
            # user_input = f"あなた: {user_input}"
            user_input = "音声を解析してください"
        elif mode == "2":
            user_input = input("あなた: ")
            audio_transcript = None
        else:
            print("無効な入力ですわよ")
            continue

        if user_input.lower() in ["exit", "quit", "またね"]:
            break
        
        response_text = connect_ai(user_input, audio_transcript)
        output(response_text)
