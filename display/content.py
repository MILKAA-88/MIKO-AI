import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
from LLM.llm import TinyLlamaWrapper
from stt.stt import record_until_silence, transcribe_audio, text_to_speech

videos = ["video/Miko-ai1.mp4", "video/Miko-ai2-1.mp4", "video/Miko-ai2-2.mp4"]
index = 0

def show_content(shutdown_event=None):
    global index

    root = tk.Tk()
    root.configure(bg="black")
    root.geometry("1080x720")

    label = tk.Label(root, bg="black")
    label.pack(expand=True)

    
    status_label = tk.Label(root, text="", font=("Helvetica", 14),
                            bg="black", fg="white", wraplength=900)
    status_label.pack(pady=(0, 20))

    
    llm = TinyLlamaWrapper()

   
    def play_video():
        global index, cap
        cap = cv2.VideoCapture(videos[index])
        def next_frame():
            global index
            
            if shutdown_event and shutdown_event.is_set():
                cap.release()
                root.destroy()
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
                play_video()
        next_frame()

    
    def voice_loop():
        while True:
            if shutdown_event and shutdown_event.is_set():
                break

            
            status_label.config(text="Listening...")
            audio_file = record_until_silence()

            
            status_label.config(text="Transcription...")
            text, lang = transcribe_audio(audio_file)

            if not text:
                status_label.config(text="❓ Error, nothing hear. Pls retry.")
                continue

            status_label.config(text=f"You said: {text}")
            print(f"[STT] {text}")

            
            status_label.config(text="MIKO AI thoughtful...")
            response = llm.generate_response(text)
            print(f"[LLM] {response}")

            
            status_label.config(text=f"MIKO AI: {response}")
            text_to_speech(response, language=lang)


    voice_thread = threading.Thread(target=voice_loop, daemon=True)
    voice_thread.start()

    play_video()
    root.mainloop()