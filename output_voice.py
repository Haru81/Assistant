import requests
import io
import soundfile
import sounddevice as sd

class Sbv2Adapter:
    URL = "http://127.0.0.1:5000/voice"

    def __init__(self) -> None:
        pass

    # 音声を取得するためのクエリ作成
    def _create_audio_query(self, text: str) -> dict:
        params = {
            "text": text,
            "speaker_id": 0,
            "model_name": "Anneli",
            "length": 1.2, # 音声の話速（1.0 = 標準、2.0 = 2倍遅く、0.5 = 2倍速く）
            "sdp_ratio": 0.2,
            "noise": 0.6,
            "noisew": 0.8,
            "auto_split": True,
            "split_interval": 1,
            "language": "JP",
            "style": "テンション高め",
            "style_weight": 5,
        }
        return params

    # 音声のリクエスト
    def _create_request_audio(self, query_data: dict) -> bytes:
        headers = {"accept": "audio/wav"}
        response = requests.get(self.URL, params=query_data, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")
        return response.content

    # 音声の取得
    def get_voice(self, text: str):
        query_data = self._create_audio_query(text)
        audio_bytes = self._create_request_audio(query_data)
        audio_stream = io.BytesIO(audio_bytes)
        data, sample_rate = soundfile.read(audio_stream)
        return data, sample_rate

