import sys
import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

BG      = "#69b4dc"
BG2     = "#f5f5f5"
TEXT    = "#FFFFFF"
DIM     = "#000000"
GREEN   = "#1a9e5c"
RED     = "#d93025"
YELLOW  = "#e8a000"
ACCENT  = "#000000"

MODULES = [
    "cv2",
    "PIL",
    "requests",
    "numpy",
    "DeepFace",
    "Gtts",
    "Whisper",
]

PIP_NAMES = {
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "requests": "requests",
    "numpy": "numpy",
    "DeepFace": "deepface",
    "Gtts": "gTTS",
    "Whisper": "openai-whisper",
}

class LoadingWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MIKO AI")
        self.root.geometry("800x520")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="MIKO AI",
                 font=("Helvetica", 32, "bold"),
                 bg=BG, fg=TEXT).pack(pady=(40, 4))

        tk.Label(self.root, text="Install all the modules required for MIKO AI. If any issues occur, please contact the admin.",
                 font=("Helvetica", 10),
                 bg=BG, fg=DIM).pack()

        tk.Frame(self.root, bg="#e0e0e0", height=1).pack(
            fill="x", padx=60, pady=20)

        self.log = scrolledtext.ScrolledText(
            self.root,
            font=("Helvetica", 11),
            bg=BG2,
            fg=TEXT,
            state="disabled",
            wrap="word",
            bd=0,
            highlightthickness=0,
        )
        self.log.pack(fill="both", expand=True, padx=60)

        self.log.tag_config("success", foreground=GREEN)
        self.log.tag_config("error", foreground=RED)
        self.log.tag_config("warning", foreground=YELLOW)
        self.log.tag_config("dim", foreground=DIM)
        self.log.tag_config("info", foreground=TEXT)

        tk.Frame(self.root, bg="#e0e0e0", height=1).pack(
            fill="x", padx=60, pady=20)

        self.progress_bar = tk.Canvas(self.root, bg=BG, height=4,
                                      highlightthickness=0)
        self.progress_bar.pack(fill="x", padx=60)

        self.percent_label = tk.Label(self.root, text="0%",
                                      font=("Helvetica", 10),
                                      bg=BG, fg=DIM)
        self.percent_label.pack(pady=(8, 24))

    def log_print(self, message: str, level: str = "info"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.config(state="normal")
        self.log.insert("end", f"[{ts}] {message}\n", level)
        self.log.see("end")
        self.log.config(state="disabled")

    def set_progress(self, value: float):
        w = self.progress_bar.winfo_width()
        self.progress_bar.delete("all")
        self.progress_bar.create_rectangle(0, 0, w, 4,
                                           fill="#e0e0e0", outline="")
        self.progress_bar.create_rectangle(0, 0, int(w * value), 4,
                                           fill=ACCENT, outline="")
        self.percent_label.config(text=f"{int(value * 100)}%")

    def check_and_install(self, module: str) -> bool:
        pip_name = PIP_NAMES.get(module, module)

        self.log_print(f"Checking {module}...", "dim")

        try:
            __import__(module)
            self.log_print(f"{module} OK ✓", "success")
            return True

        except ImportError:
            self.log_print(f"{module} missing → installing {pip_name}...", "warning")

            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", pip_name],
                    capture_output=True,
                    text=True
                )

                # stdout
                if result.stdout:
                    for line in result.stdout.splitlines():
                        if line.strip():
                            self.log_print(line, "dim")

                
                if result.stderr:
                    self.log_print("---- PIP ERROR ----", "error")
                    for line in result.stderr.splitlines():
                        if line.strip():
                            self.log_print(line, "error")

                if result.returncode == 0:
                    self.log_print(f"{module} installed successfully ✓", "success")
                    return True
                else:
                    self.log_print(
                        f"{module} install failed (code {result.returncode}) ✗",
                        "error"
                    )
                    return False

            except Exception as e:
                self.log_print(f"Critical error: {e}", "error")
                return False

    def _load_thread(self):
        self.log_print("Starting system...", "dim")

        total = len(MODULES)
        success = 0

        for i, module in enumerate(MODULES):
            if self.check_and_install(module):
                success += 1

            progress = (i + 1) / total
            self.root.after(0, lambda p=progress: self.set_progress(p))

        if success == total:
            self.log_print("All modules are ready/installed, bye!", "success")
            self.root.after(12000, self.root.destroy)
        else:
            self.log_print(f"{total - success} module(s) failed. Contact the admin.", "error")
            self.root.after(15000, self.root.destroy)

    def run(self):
        threading.Thread(target=self._load_thread, daemon=True).start()
        self.root.mainloop()


def show_loading():
    LoadingWindow().run()


if __name__ == "__main__":
    show_loading()