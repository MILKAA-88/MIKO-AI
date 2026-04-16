import whisper
from gtts import gTTS
import os
import pyaudio
import wave
import numpy as np

RATE = 16000
CHUNK = 1024
SILENCE_LIMIT = 7
SILENCE_THRESHOLD = 500
OUTPUT_FILE = "user_input.wav"

model = whisper.load_model("small")

def record_until_silence():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Listening...")
    frames = []
    silence_chunks = 0
    max_silence_chunks = int(RATE / CHUNK * SILENCE_LIMIT)

    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        amplitude = np.frombuffer(data, dtype=np.int16)
        if np.abs(amplitude).mean() < SILENCE_THRESHOLD:
            silence_chunks += 1
        else:
            silence_chunks = 0
        if silence_chunks >= max_silence_chunks:
            print("Silence detected, starting transcription...")
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(OUTPUT_FILE, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

while True:
  
    record_until_silence()

    
    result = model.transcribe(
        OUTPUT_FILE,
        fp16=False,
        verbose=True,
        word_timestamps=True
    )

    
    text = result["text"]
    detected_language = result["language"]
    print(f"Language detected: {detected_language}")
    print(f"Text: {text}")

    
    choice = input("Wanna continue? Y or N: ").strip().upper()

    if choice == "N":
        break

    if choice == "Y":
        tts = gTTS(text=text, lang=detected_language, slow=False)
        tts.save("response.mp3")
        os.system("start response.mp3")