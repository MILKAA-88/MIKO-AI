import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
index = 0 

videos = [
    os.path.join(BASE_DIR, "video", "Miko-ai1.mp4"),
    os.path.join(BASE_DIR, "video", "Miko-ai2-1.mp4"),
    os.path.join(BASE_DIR, "video", "Miko-ai2-2.mp4")
]

def show_content():
    global index
    root = tk.Tk()
    root.configure(bg="black")
    root.geometry("1080x720")
    label = tk.Label(root, bg="black")
    label.pack(expand=True)

    def play_video():
        global index, cap
        cap = cv2.VideoCapture(videos[index])

        def next_frame():
            global index
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

    play_video()       
    root.mainloop()    

if __name__ == "__main__":
    show_content()     