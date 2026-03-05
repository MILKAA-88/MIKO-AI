import whisper
import sounddevice as sd
from scipy.io.wavfile import write

# Chargement du modèle (tiny = rapide, base = équilibré, large = précis)
model = whisper.load_model("base")

# Enregistrement micro (5 secondes)
DUREE = 5
SAMPLE_RATE = 16000

print("Speak now...")
audio = sd.rec(int(DUREE * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
sd.wait()
write("temp_audio.wav", SAMPLE_RATE, audio)


result = model.transcribe("temp_audio.wav", language="fr")
print("U said:", result["text"])