import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import whisper
import pyaudio
import numpy as np
import subprocess
import asyncio
import edge_tts

RATE = 16000
CHUNK = 1024
SILENCE_LIMIT = 7
SILENCE_THRESHOLD = 500
VOICE = "fr-FR-HenriNeural"

whisper_model = whisper.load_model("base")

def record_until_silence():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    print("Listening...")
    frames = []
    silence_chunks = 0
    max_silence_chunks = int(RATE / CHUNK * SILENCE_LIMIT)
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            amplitude = np.frombuffer(data, dtype=np.int16)
            if np.abs(amplitude).mean() < SILENCE_THRESHOLD:
                silence_chunks += 1
            else:
                silence_chunks = 0
            if silence_chunks >= max_silence_chunks:
                print("Silence detected, recording stopped.")
                break
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
    return b"".join(frames)

def transcribe(audio_bytes):
    import tempfile, wave
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        with wave.open(f, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(RATE)
            wf.writeframes(audio_bytes)
        tmp_path = f.name
    result = whisper_model.transcribe(tmp_path, language="fr")
    os.remove(tmp_path)
    return result["text"].strip()

async def generate_speech(text, output_path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)

def tts(text):
    output_path = 'response_llm.mp3'
    asyncio.run(generate_speech(text, output_path))
    return output_path

def play_audio(path):
    subprocess.run(["mpv", "--no-terminal", path])