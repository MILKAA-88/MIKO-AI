from tkinter import *
import requests

root = Tk()
root.geometry("1080x720")
root.minsize(480, 360)
root.config(background="#000000")

label_title = Label(root, text="MIKO AI checks if everything is operational.", font=("Lato", 20), fg="white", bg="#000000")
label_title.place(x=540, y=360, anchor="center")

taille_police = 24
pos_y = 360

def animate():
    global taille_police, pos_y
    if pos_y > 50 and taille_police > 12:
        pos_y -= 3
        taille_police -= 0.3
        label_title.place(x=540, y=int(pos_y), anchor="center")
        label_title.config(font=("Lato", int(taille_police)))
        root.after(16, animate)
    else:
        start()

def start():
    labelping = Label(root, text="Ping google", font=("Lato", 20), fg="white", bg="#000000")
    labelping.place(x=540, y=200, anchor="center")

    def ping():
        try:
            response = requests.get("https://www.google.com/", timeout=5)
            if response.status_code == 200:
                result = Label(root, text="Perfect! An internet connection has been recognized", font=("Lato", 20), fg="white", bg="#000000")
                result.place(x=540, y=250, anchor="center")
            else:
                result = Label(root, text=f"⚠️ Status code: {response.status_code}", font=("Lato", 20), fg="white", bg="#000000")
                result.place(x=540, y=250, anchor="center")
        except requests.ConnectionError:
            result = Label(root, text="We could not detect/recognize your internet connection...", font=("Lato", 20), fg="white", bg="#000000")
            result.place(x=540, y=250, anchor="center")
        except requests.Timeout:
            result = Label(root, text="❌ Timeout", font=("Lato", 20), fg="white", bg="#000000")
            result.place(x=540, y=250, anchor="center")

    ping()
    root.after(5000, root.destroy)  

root.after(5000, animate)
root.mainloop()