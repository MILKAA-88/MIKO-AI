import tkinter as tk
import pyttsx3
import threading
import requests
import json
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import whisper

# ============================================================
# CONFIG
# ============================================================
WIDTH, HEIGHT   = 300, 380
BG_COLOR        = "#0a0a0a"
FACE_BORDER     = "#ffffff"
SAMPLE_RATE     = 16000
LM_STUDIO_URL   = "http://127.0.0.1:1234/v1/chat/completions"
WHISPER_MODEL   = "base"

# Seuil d'énergie sonore (ajuste si trop sensible ou pas assez)
ENERGY_THRESHOLD = 500
SILENCE_LIMIT    = 30   # frames de silence avant d'arrêter
FRAME_SIZE       = 1024

# ============================================================
# MOTEUR VOCAL
# ============================================================
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.7)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Hortense FR

# ============================================================
# WHISPER
# ============================================================
print("Chargement de Whisper...")
whisper_model = whisper.load_model(WHISPER_MODEL)
print("Whisper prêt !")

# ============================================================
# EXPRESSIONS
# ============================================================
EXPRESSIONS = {
    "heureux":   {"oeil": "heureux",   "bouche": "sourire", "sourcil": "normal"},
    "triste":    {"oeil": "triste",    "bouche": "triste",  "sourcil": "triste"},
    "surpris":   {"oeil": "surpris",   "bouche": "o",       "sourcil": "surpris"},
    "reflexion": {"oeil": "reflexion", "bouche": "ligne",   "sourcil": "reflexion"},
    "parler":    {"oeil": "normal",    "bouche": "parler",  "sourcil": "normal"},
    "neutre":    {"oeil": "normal",    "bouche": "ligne",   "sourcil": "normal"},
    "ecoute":    {"oeil": "surpris",   "bouche": "ligne",   "sourcil": "surpris"},
}

# ============================================================
# AVATAR
# ============================================================
class MikoAvatar:
    def __init__(self, root):
        self.root = root
        self.root.title("MIKO AI")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT-80,
                                bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.status_var = tk.StringVar(value="Chargement...")
        self.status_label = tk.Label(root, textvariable=self.status_var,
                                     bg=BG_COLOR, fg="#00e5ff",
                                     font=("Courier", 9), wraplength=280)
        self.status_label.pack(pady=4)

        self.text_var = tk.StringVar(value="")
        self.text_label = tk.Label(root, textvariable=self.text_var,
                                   bg=BG_COLOR, fg="white",
                                   font=("Courier", 8), wraplength=280)
        self.text_label.pack(pady=2)

        self.expression    = "neutre"
        self.blink         = False
        self.parler_ouvert = False
        self.tick          = 0
        self.is_speaking   = False

        self.draw()
        self.loop()

    def set_expression(self, expr):
        if expr in EXPRESSIONS:
            self.expression = expr

    def set_status(self, text):
        self.status_var.set(text)

    def set_text(self, text):
        self.text_var.set(text[:120] + "..." if len(text) > 120 else text)

    def parler(self, texte, expression="parler"):
        def _run():
            self.is_speaking = True
            self.set_expression(expression)
            self.set_status("MIKO parle...")
            self.set_text(texte)
            engine.say(texte)
            engine.runAndWait()
            self.is_speaking = False
            self.set_expression("neutre")
            self.set_status("🎤 Je t'écoute...")

        threading.Thread(target=_run, daemon=True).start()

    def draw(self):
        self.canvas.delete("all")
        cx = WIDTH // 2
        cy = (HEIGHT - 80) // 2
        expr = EXPRESSIONS[self.expression]

        self.canvas.create_oval(cx-110, cy-110, cx+110, cy+110,
                                fill="#0e1a2a", outline=FACE_BORDER, width=2)
        self.draw_sourcils(cx, cy, expr["sourcil"])
        self.draw_oeil(cx - 40, cy - 15, expr["oeil"], "gauche")
        self.draw_oeil(cx + 40, cy - 15, expr["oeil"], "droit")
        self.canvas.create_oval(cx-4, cy+18, cx+4, cy+26, fill="#aaaacc", outline="")
        self.draw_bouche(cx, cy + 50, expr["bouche"])
        self.canvas.create_oval(cx-75, cy+10, cx-45, cy+35, fill="#ff6b9d", stipple="gray25", outline="")
        self.canvas.create_oval(cx+45, cy+10, cx+75, cy+35, fill="#ff6b9d", stipple="gray25", outline="")
        self.canvas.create_text(cx, (HEIGHT-80) - 15, text="MIKO AI",
                                fill=FACE_BORDER, font=("Courier", 10, "bold"))

    def draw_sourcils(self, cx, cy, style):
        y = cy - 52
        if style == "normal":
            self.canvas.create_line(cx-60, y, cx-22, y, fill="white", width=2)
            self.canvas.create_line(cx+22, y, cx+60, y, fill="white", width=2)
        elif style == "triste":
            self.canvas.create_line(cx-60, y-6, cx-22, y+2, fill="white", width=2)
            self.canvas.create_line(cx+22, y+2, cx+60, y-6, fill="white", width=2)
        elif style == "surpris":
            self.canvas.create_line(cx-60, y-8, cx-22, y-8, fill="white", width=2)
            self.canvas.create_line(cx+22, y-8, cx+60, y-8, fill="white", width=2)
        elif style == "reflexion":
            self.canvas.create_line(cx-60, y, cx-22, y-5, fill="white", width=2)
            self.canvas.create_line(cx+22, y-5, cx+60, y+2, fill="white", width=2)

    def draw_oeil(self, x, y, style, cote):
        if self.blink:
            self.canvas.create_line(x-18, y, x+18, y, fill="white", width=3)
            return
        if style == "normal":
            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill="#111122", outline="white", width=2)
            self.canvas.create_oval(x-8, y-8, x+8, y+8, fill="white", outline="")
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="#111122", outline="")
        elif style == "heureux":
            self.canvas.create_arc(x-18, y-10, x+18, y+18, start=0, extent=180,
                                   style=tk.ARC, outline="white", width=3)
        elif style == "triste":
            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill="#111122", outline="white", width=2)
            self.canvas.create_oval(x-8, y-4, x+8, y+12, fill="white", outline="")
            self.canvas.create_oval(x+8, y+14, x+16, y+26, fill="#00aaff", outline="")
        elif style == "surpris":
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="#111122", outline="white", width=3)
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="white", outline="")
        elif style == "reflexion":
            if cote == "gauche":
                self.canvas.create_oval(x-18, y-18, x+18, y+18, fill="#111122", outline="white", width=2)
                self.canvas.create_oval(x-4, y-8, x+12, y+8, fill="white", outline="")
            else:
                self.canvas.create_arc(x-18, y-18, x+18, y+18, start=200, extent=140,
                                       style=tk.ARC, outline="white", width=2)

    def draw_bouche(self, x, y, style):
        if style == "parler":
            ouverture = 12 if self.parler_ouvert else 4
            self.canvas.create_oval(x-20, y-ouverture, x+20, y+ouverture,
                                    fill="#cc3366", outline="white", width=2)
            return
        if style == "sourire":
            self.canvas.create_arc(x-30, y-20, x+30, y+20, start=200, extent=140,
                                   style=tk.ARC, outline="white", width=3)
        elif style == "triste":
            self.canvas.create_arc(x-30, y-10, x+30, y+30, start=20, extent=140,
                                   style=tk.ARC, outline="white", width=3)
        elif style == "o":
            self.canvas.create_oval(x-14, y-14, x+14, y+14,
                                    fill="#cc3366", outline="white", width=2)
        elif style == "ligne":
            self.canvas.create_line(x-22, y, x+22, y, fill="white", width=3)

    def loop(self):
        self.tick += 1
        if self.tick % 90 == 0:
            self.blink = True
            self.root.after(120, self.stop_blink)
        if self.expression == "parler" and self.tick % 8 == 0:
            self.parler_ouvert = not self.parler_ouvert
        self.draw()
        self.root.after(33, self.loop)

    def stop_blink(self):
        self.blink = False


# ============================================================
# LM STUDIO
# ============================================================
historique = []

def demander_llm(texte):
    historique.append({"role": "user", "content": texte})

    system_prompt = """Tu es MIKO AI, un assistant virtuel kawaii, sympathique et expressif.
Réponds UNIQUEMENT en JSON avec ce format exact, sans texte avant ou après :
{
  "reponse": "ta réponse ici",
  "emotion": "heureux|triste|surpris|reflexion|neutre"
}
Choisis l'émotion qui correspond le mieux à ta réponse."""

    try:
        response = requests.post(LM_STUDIO_URL, json={
            "model": "local-model",
            "messages": [{"role": "system", "content": system_prompt}] + historique,
            "temperature": 0.7
        }, timeout=30)

        content = response.json()["choices"][0]["message"]["content"]
        print(f"Réponse brute LLM : {content}")  # ← debug
        content = content.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        reponse = data.get("reponse", "Je n'ai pas compris.")
        emotion = data.get("emotion", "neutre")

        historique.append({"role": "assistant", "content": reponse})
        return reponse, emotion

    except Exception as e:
        print(f"Erreur LLM : {e}")
        return "Désolé, je n'ai pas pu répondre.", "triste"


# ============================================================
# DÉTECTION D'ÉNERGIE SONORE (sans C++)
# ============================================================
def energie(frame):
    """Calcule l'énergie RMS d'un frame audio"""
    return np.sqrt(np.mean(frame.astype(np.float32) ** 2))

def ecouter_et_transcrire(avatar):
    print("Micro actif, je t'écoute...")

    while True:
        # Ne pas écouter si MIKO est en train de parler
        if avatar.is_speaking:
            import time
            time.sleep(0.1)
            continue

        avatar.set_status("🎤 Je t'écoute...")
        avatar.set_expression("ecoute")

        frames       = []
        silence_count = 0
        speaking     = False

        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1,
                            dtype='int16', blocksize=FRAME_SIZE) as stream:
            while True:
                frame, _ = stream.read(FRAME_SIZE)
                frame_np  = np.array(frame).flatten()
                e = energie(frame_np)

                if e > ENERGY_THRESHOLD:
                    speaking      = True
                    silence_count = 0
                    frames.append(frame_np)
                elif speaking:
                    silence_count += 1
                    frames.append(frame_np)
                    if silence_count > SILENCE_LIMIT:
                        break

        if not frames or not speaking:
            continue

        # Sauvegarde audio
        audio = np.concatenate(frames)
        write("temp_audio.wav", SAMPLE_RATE, audio)

        # Transcription Whisper
        avatar.set_status("⏳ Transcription...")
        avatar.set_expression("reflexion")
        result = whisper_model.transcribe("temp_audio.wav", language="fr")
        texte  = result["text"].strip()

        if not texte:
            continue

        print(f"Toi : {texte}")
        avatar.set_text(f"Toi : {texte}")

        # LM Studio
        avatar.set_status("🧠 Réflexion...")
        reponse, emotion = demander_llm(texte)
        print(f"MIKO : {reponse} [{emotion}]")

        # Parler + animer
        avatar.parler(reponse, emotion)


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    avatar = MikoAvatar(root)

    thread = threading.Thread(target=ecouter_et_transcrire, args=(avatar,), daemon=True)
    thread.start()

    avatar.parler("Bonjour ! Je suis MIKO AI. Parle-moi, je t'écoute !", "heureux")
    root.mainloop()