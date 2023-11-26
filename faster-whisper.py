# pip install faster-whisper sounddevice
# ZIP - Datei von https://github.com/Purfview/whisper-standalone-win/releases/tag/libs herunterladen und in PATH packen

import sounddevice as sd
import numpy as np
import queue
from faster_whisper import WhisperModel

# Lade das Faster-Whisper-Modell
model_size = "large-v2"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# Erstelle eine Warteschlange, um die Audiodaten zu speichern
q = queue.Queue()

def callback(indata, frames, time, status):
    """Diese Funktion wird für jeden Audio-Block aufgerufen."""
    q.put(indata.copy())

# Starte die Aufnahme
with sd.InputStream(callback=callback, channels=1, samplerate=16000):
    buffer = np.array([])
    while True:
        # Hole die Audiodaten aus der Warteschlange
        data = q.get()
        
        # Konvertiere die Audiodaten in ein Numpy-Array
        audio = np.frombuffer(data, dtype=np.int16)
        
        # Füge die neuen Audiodaten zum Puffer hinzu
        buffer = np.concatenate((buffer, audio))
        
        # Wenn der Puffer 5 Sekunden Audio enthält
        if len(buffer) >= 5 * 16000:
            print("5 Sekunden sind rum, transkribiere ...")
            # Transkribiere das Audio
            segments, info = model.transcribe(buffer[:5*16000], beam_size=5, language="de")
            
            # Gib das Ergebnis auf der Konsole aus
            for segment in segments:
                print(" [%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            
            # Entferne das transkribierte Audio aus dem Puffer
            buffer = buffer[5*16000:]