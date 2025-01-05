import sounddevice as sd
import wave

class SoundRecognizer:
    def __init__(self):
    # 音声設定
        self.RATE = 44100
        self.CHANNELS = 1
        self.DURATION = 5
        self.OUTPUT_FILENAME = "record.wav"

    def record(self):
    # 録音処理
        recording = sd.rec(int(self.DURATION * self.RATE), samplerate=self.RATE, channels=self.CHANNELS, dtype="int16")
        sd.wait()

    def save(self):
    # WAVファイルに保存
        with wave.open(self.OUTPUT_FILENAME, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(self.RATE)
            wf.writeframes(self.recording.tobytes())
