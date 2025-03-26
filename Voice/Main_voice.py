# ---------- ↓ --- Импорт библиотек --- ↓ --------------------------------------------------
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import pyttsx3
import json
import pyaudio
import time
import torch
import json

engine = pyttsx3.init()

# ---------- ↓ --- Настройка модуля Vosk --- ↓ ---------------------------------------------
model = Model('Voice/model_small')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1,
                rate=16000, input=True, frames_per_buffer=8000)

# ---------- ↓ --- Преобразование голоса в текст --- ↓ -------------------------------------
def stt(mod: bool = False):
    with open("Settings/Main_settings.json", "r", encoding="utf-8") as MS_file:
        time_sleep = json.load(MS_file)["Time_sleep"]
    stream.start_stream()
    start_time = time.time()  # Запись времени старта функции
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(rec.Result())
            if answer['text']:
                stream.stop_stream()
                return answer['text']
        if (time.time() - start_time) >= time_sleep and mod == False:
            return "sleep"

# ==========================================================================================

language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'aidar' #aidar, baya, kseniya, xenia, random
device = torch.device('cpu')

model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
model.to(device)  # gpu or cpu

def tts_2(text):
    engine.say(text=text)
    engine.runAndWait()

def tts(text, mod=False):
    audio = model.apply_tts(text=text+"....",
                        speaker=speaker,
                        sample_rate=sample_rate)
    if mod == False:
        sd.play(audio, sample_rate * 1.2)
        time.sleep((len(audio) / sample_rate) * 1.2 + 0.6)
        sd.stop()

for i in range(0, 5):
    tts(text="Привет", mod=True)
