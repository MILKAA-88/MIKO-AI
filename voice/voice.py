import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import threading
import platform
import pygame  

def transcribe_audio(output_wav="temp_audio.wav"):
    SAMPLE_RATE = 16000
    frames = []

    def record():
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16') as stream:
            print("Record current... Press Enter.")
            while getattr(record, "recording", True):
                data, _ = stream.read(1024)
                frames.append(data)

    record.recording = True
    thread = threading.Thread(target=record)
    thread.start()
    input()
    record.recording = False
    thread.join()

    audio = np.concatenate(frames, axis=0)
    write(output_wav, SAMPLE_RATE, audio)

    model = whisper.load_model("small")
    result = model.transcribe(output_wav, language="fr")
    os.remove(output_wav)
    return result["text"]

def play_audio(file_path):
    try:
        
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error pygame : {e}")
        if platform.system() == "Windows":
            os.system(f"start {file_path}")
        else:
            os.system(f"xdg-open {file_path}")
    finally:
        os.remove(file_path)  