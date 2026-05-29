import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
from LLM.llm import LLM
from stt_tts.stt_tts import record_until_silence, transcribe, tts, play_audio
from face.face_detection import start_face_detection

shutdown_event = threading.Event()
face_thread = threading.Thread(target=start_face_detection, args=(shutdown_event,))
face_thread.daemon = True
face_thread.start()

videos = ["video/Miko-ai1.mp4"]
index = 0

def show_content():
    global index
    root = tk.Tk()
    root.configure(bg="black")
    root.geometry("1080x720")

    label = tk.Label(root, bg="black")
    label.pack(expand=True)

    status_label = tk.Label(root, text="", font=("Lato", 14),
                            bg="black", fg="white", wraplength=900)
    status_label.pack(pady=(0, 20))

    llm = LLM()

    def set_status(text):
        root.after(0, lambda: status_label.config(text=text))

    def check_shutdown():
        shutdown_event.wait()
        print("Bye")
        root.after(0, root.destroy)
    threading.Thread(target=check_shutdown, daemon=True).start()

    def play_video():
        global index
        cap = cv2.VideoCapture(videos[index])

        def next_frame():
            global index
            if shutdown_event.is_set():
                cap.release()
                root.after(0, root.destroy)
                return
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                label.config(image=img)
                label.image = img
                root.after(30, next_frame)
            else:
                cap.release()
                index = (index + 1) % len(videos)
                root.after(0, play_video)  

        next_frame()

    def voice_loop():
        while not shutdown_event.is_set():
            set_status("Écoute en cours...")
            audio_bytes = record_until_silence()
            if shutdown_event.is_set():
                break
            set_status("Transcription...")
            text = transcribe(audio_bytes)
            if not text:
                set_status("Rien entendu, veuillez réessayer.")
                continue
            set_status(f"You said: {text}")
            print(f"[STT] {text}")
            set_status("MIKO réfléchit...")
            response = llm.generate_response(text)
            print(f"[LLM] {response}")
            set_status(f"MIKO AI : {response}")
            audio_path = tts(response)
            play_audio(audio_path)

    voice_thread = threading.Thread(target=voice_loop, name="voice_loop", daemon=True)
    voice_thread.start()

    play_video()
    root.mainloop()