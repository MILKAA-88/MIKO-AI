import tkinter as tk
import pyttsx3
import threading

# --- Configuration ---
WIDTH, HEIGHT = 300, 300
BG_COLOR = "#0a0a0a"
FACE_BORDER = "#00e5ff"

# --- Moteur vocal ---
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Hortense - Français

# --- Expressions ---
EXPRESSIONS = {
    "heureux":   {"oeil": "heureux",   "bouche": "sourire", "sourcil": "normal"},
    "triste":    {"oeil": "triste",    "bouche": "triste",  "sourcil": "triste"},
    "surpris":   {"oeil": "surpris",   "bouche": "o",       "sourcil": "surpris"},
    "reflexion": {"oeil": "reflexion", "bouche": "ligne",   "sourcil": "reflexion"},
    "parler":    {"oeil": "normal",    "bouche": "parler",  "sourcil": "normal"},
    "neutre":    {"oeil": "normal",    "bouche": "ligne",   "sourcil": "normal"},
}

class MikoAvatar:
    def __init__(self, root):
        self.root = root
        self.root.title("MIKO AI")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.expression = "neutre"
        self.blink = False
        self.parler_ouvert = False
        self.tick = 0
        self.is_speaking = False

        self.draw()
        self.loop()

    def set_expression(self, expr):
        if expr in EXPRESSIONS:
            self.expression = expr

    def parler(self, texte, expression="parler"):
        """Fait parler MIKO avec animation de bouche"""
        def _run():
            self.is_speaking = True
            self.set_expression(expression)
            engine.say(texte)
            engine.runAndWait()
            self.is_speaking = False
            self.set_expression("neutre")

        threading.Thread(target=_run, daemon=True).start()

    def draw(self):
        self.canvas.delete("all")
        cx, cy = WIDTH // 2, HEIGHT // 2
        expr = EXPRESSIONS[self.expression]

        # Fond
        self.canvas.create_oval(cx-110, cy-110, cx+110, cy+110,
                                fill="#0e1a2a", outline=FACE_BORDER, width=2)

        # Sourcils
        self.draw_sourcils(cx, cy, expr["sourcil"])

        # Yeux
        self.draw_oeil(cx - 40, cy - 15, expr["oeil"], "gauche")
        self.draw_oeil(cx + 40, cy - 15, expr["oeil"], "droit")

        # Nez
        self.canvas.create_oval(cx-4, cy+18, cx+4, cy+26, fill="#aaaacc", outline="")

        # Bouche
        self.draw_bouche(cx, cy + 50, expr["bouche"])

        # Joues
        self.canvas.create_oval(cx-75, cy+10, cx-45, cy+35, fill="#ff6b9d", stipple="gray25", outline="")
        self.canvas.create_oval(cx+45, cy+10, cx+75, cy+35, fill="#ff6b9d", stipple="gray25", outline="")

        # Nom
        self.canvas.create_text(cx, HEIGHT - 20, text="MIKO AI",
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

        # Clignement toutes les ~3 secondes
        if self.tick % 90 == 0:
            self.blink = True
            self.root.after(120, self.stop_blink)

        # Animation bouche parler
        if self.expression == "parler" and self.tick % 8 == 0:
            self.parler_ouvert = not self.parler_ouvert

        self.draw()
        self.root.after(33, self.loop)

    def stop_blink(self):
        self.blink = False


# --- Lancement ---
if __name__ == "__main__":
    root = tk.Tk()
    avatar = MikoAvatar(root)

    # Test voix + expressions
    def demo():
        avatar.root.after(500,  lambda: avatar.parler("Bonjour ! Je suis MIKO AI, votre assistant virtuel.", "heureux"))
        avatar.root.after(4000, lambda: avatar.parler("Je réfléchis à votre demande.", "reflexion"))
        avatar.root.after(7000, lambda: avatar.parler("Oh ! Je suis surpris !", "surpris"))
        avatar.root.after(9500, lambda: avatar.parler("Je suis un peu triste aujourd'hui.", "triste"))

    root.after(500, demo)
    root.mainloop()

   