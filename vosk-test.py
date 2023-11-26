# pip install vosk sounddevice
# Sprachmodell von https://alphacephei.com/vosk/models herunterladen

import os
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Pfad zum Vosk-Modell
model_path = "./vosk-model-de-tuda-0.6-900k"
if not os.path.exists(model_path):
    print("Bitte geben Sie den korrekten Pfad zum Vosk-Modell an.")
    exit(1)

# Lade Vosk-Modell
model = Model(model_path)

# Erstelle eine Warteschlange, um die Audiodaten zu speichern
q = queue.Queue()

def callback(indata, frames, time, status):
    """Diese Funktion wird für jeden Audio-Block aufgerufen."""
    q.put(bytes(indata))

# Starte die Aufnahme
with sd.InputStream(callback=callback, channels=1, samplerate=16000):
    rec = KaldiRecognizer(model, 16000)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            print(result)