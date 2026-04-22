import whisper
from gtts import gTTS
import os
import pyaudio
import wave
import numpy as np
import tempfile
import subprocess
import time


RATE = 16000
CHUNK = 1024
SILENCE_LIMIT = 7
SILENCE_THRESHOLD = 500


model = whisper.load_model("small")


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
                print("Silence détecté, arrêt de l'enregistrement.")
                break
    finally:
        stream.stop_stream()
        stream.close()
       
        sample_width = audio.get_sample_size(pyaudio.paInt16)
        audio.terminate()

    # Écrire dans un fichier temporaire
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    output_file = tmp.name
    tmp.close()

    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return output_file


def transcribe_audio(audio_file):

    if not audio_file or not os.path.exists(audio_file):
        print(f"[Transcription] file not found: {audio_file}")
        return "", "fr"

    result = model.transcribe(
        audio_file,
        fp16=False,
        verbose=False,
        word_timestamps=True
    )

    text = result.get("text", "").strip()
    language = result.get("language", "fr")


    try:
        os.remove(audio_file)
    except OSError:
        pass

    if not text:
        return "", language

    return text, language


def text_to_speech(text, language="fr"):

    if not text:
        return ""


    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    output_path = tmp.name
    tmp.close()

    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_path)


    proc = subprocess.Popen(
        ["start", "/wait", "", output_path],
        shell=True
    )
    proc.wait()


    time.sleep(0.5)
    try:
        os.remove(output_path)
    except OSError:
        pass

    return output_path