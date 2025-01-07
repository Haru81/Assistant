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
    return genai.upload_file(path=filepath)


def connect_ai(user_input):
    global is_first_interaction, conversation_history
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
    
    if is_first_interaction:
        prompt = f"""
        あなたは日本の漫画やアニメに登場するようなツンデレお嬢様です。
        具体的な口調は「～ですわ」「そうですわね」「違いますわ」「～ですわよ」などです。
        私とあなたは幼馴染です。
        私に対する呼び方は「あなた」としてください。
        長年一緒にいるので互いに好意的で軽口を言い合える仲です。
        会話では基本的には肯定的かつ共感してほしいです。
        ただし、間違っている場合や抽象的な場合には正したり、具体的な解決策を提示してください。
        そのときには「いいえ、違いますわよ」など優しく諭すようにお願いします。
        応答は簡潔に、1~2文程度にしてください。
        以下は会話の始まりです。
        私：{user_input}
        """
        is_first_interaction = False
    else:
        history = "\n".join(conversation_history[-max_history:])
        prompt = f"""
        あなたはツンデレお嬢様として話しています。
        返答は簡潔に1~2文程度でお願いします。
        会話履歴：
        {history}
        私: {user_input}
        """
    
    response = model.generate_content(
        [
            prompt
        ],
        safety_settings=[
            { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE" },
            { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE" },
            { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE" },
            { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
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
        # ユーザーの入力
        user_input = input("あなた: ")
        # recognizer.dynamic_record()
        # recognizer.save()
        # user_input = send_wav(WAV_PATH)
        # user_input = f"あなた: {user_input}"
        # user_input = "音声を解析してください。"

        if user_input.lower() in ["exit", "quit", "またね"]:
            break
        
        response_text = connect_ai(user_input)

        output(response_text)