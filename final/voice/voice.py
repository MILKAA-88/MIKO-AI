import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import threading

SAMPLE_RATE = 16000
frames = []
recording = True

def record():
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16') as stream:
        while recording:
            data, _ = stream.read(1024)
            frames.append(data)

# Démarre l'enregistrement dans un thread séparé
thread = threading.Thread(target=record)
thread.start()

print("Recording in progress... Press Enter for stop.")
input()

recording = False
thread.join()

# Sauvegarde et transcription
audio = np.concatenate(frames, axis=0)
write("temp_audio.wav", SAMPLE_RATE, audio)

model = whisper.load_model("small") 
result = model.transcribe("temp_audio.wav", language="fr")
print("You said:", result["text"])