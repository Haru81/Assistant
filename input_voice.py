import sounddevice as sd
import wave
import os
import numpy as np
import time
import keyboard

class SoundRecognizer:
    def __init__(self):
    # 音声設定
        self.RATE = 44100
        self.CHANNELS = 1
        self.DURATION = 5
        self.OUTPUT_DIR = "media"
        self.OUTPUT_FILENAME = os.path.join(self.OUTPUT_DIR, "record.wav")
        self.recording = None

        # フォルダが存在しない場合
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)


    def static_record(self):
    # 録音処理
        self.recording = sd.rec(int(self.DURATION * self.RATE), samplerate=self.RATE, channels=self.CHANNELS, dtype="int16")
        sd.wait()


    def dynamic_record(self):
        max_duration = 10
        threshold = 500
        silence_duration = 2

        audio = []
        silence_start = None
        start_time = time.time()
        stream = sd.InputStream(samplerate=self.RATE, channels=self.CHANNELS, dtype="int16")
        
        with stream:
            # for _ in range(int(max_duration * self.RATE / 1024)):
            while time.time() - start_time < max_duration:
                data, _ = stream.read(1024)
                audio.extend(data.flatten())

                # 無音判定
                if np.abs(data).max() < threshold:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start >= silence_duration:
                        break
                else:
                    silence_start = None

        self.recording = np.array(audio, dtype="int16")


    def record_with_space_key(self):
        """スペースキーを押すと録音停止"""
        print("recording start(please stop space key)...")
        audio = []
        stream = sd.InputStream(samplerate=self.RATE, channels=self.CHANNELS, dtype="int16")

        with stream:
            while True:
                data, _ = stream.read(1024)
                audio.extend(data.flatten())

                if keyboard.is_pressed("space"):
                    print("stop recording")
                    break
        self.recording = np.array(audio, dtype="int16")


    def save(self):
        # WAVファイルに保存
        if self.recording is not None:
            with wave.open(self.OUTPUT_FILENAME, "wb") as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(self.RATE)
                wf.writeframes(self.recording.tobytes())
        else:
            print("録音データがありません。")

