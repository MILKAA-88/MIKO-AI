import os
import sys
import time
import subprocess
import threading
import requests
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

GITHUB_USER = "MILKAA-88"
GITHUB_REPO = "MIKO-AI"
BRANCH = "main"
VERSION_FILE = ".miko_version"
CHECK_INTERVAL = 20


BG        = "#0d0f1a"
BG2       = "#151728"
ACCENT    = "#4f8ef7"
GREEN     = "#3ddc84"
YELLOW    = "#f7c948"
RED       = "#f75f5f"
TEXT      = "#cdd6f4"
TEXT_DIM  = "#585b70"

class UpdaterWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MIKO-AI — Updater")
        self.root.geometry("800x520")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self._build_ui()
        self._updating = False

    def _build_ui(self):
        # ── Header ──
        header = tk.Frame(self.root, bg=BG2, height=48)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="⟳  MIKO-AI Updater",
                 font=("Consolas", 13, "bold"),
                 bg=BG2, fg=ACCENT).pack(side="left", padx=16, pady=12)

        self.status_label = tk.Label(header, text="● Online",
                                     font=("Consolas", 10),
                                     bg=BG2, fg=GREEN)
        self.status_label.pack(side="right", padx=16)

        # ── Log zone ──
        self.log = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 10),
            bg=BG, fg=TEXT,
            insertbackground=TEXT,
            relief="flat", bd=0,
            padx=12, pady=8,
            state="disabled",
            wrap="word"
        )
        self.log.pack(fill="both", expand=True, padx=0, pady=0)

      
        self.log.tag_config("info",    foreground=TEXT)
        self.log.tag_config("success", foreground=GREEN)
        self.log.tag_config("warning", foreground=YELLOW)
        self.log.tag_config("error",   foreground=RED)
        self.log.tag_config("dim",     foreground=TEXT_DIM)
        self.log.tag_config("accent",  foreground=ACCENT)

        
        prog_frame = tk.Frame(self.root, bg=BG2, height=32)
        prog_frame.pack(fill="x")
        prog_frame.pack_propagate(False)

        self.progress_bar = tk.Canvas(prog_frame, bg=BG2,
                                      height=4, highlightthickness=0)
        self.progress_bar.pack(fill="x", pady=14, padx=16)
        self._prog_rect = None
        self._anim_pos  = 0

    # ─── Logging ────────────────────────────────────────
    def log_print(self, message: str, level: str = "info"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.config(state="normal")
        self.log.insert("end", f"[{ts}] ", "dim")
        self.log.insert("end", f"{message}\n", level)
        self.log.see("end")
        self.log.config(state="disabled")

    
    def _animate_progress(self):
        if not self._updating:
            self.progress_bar.delete("all")
            return
        w = self.progress_bar.winfo_width()
        bw = 120
        self._anim_pos = (self._anim_pos + 6) % (w + bw)
        x1 = self._anim_pos - bw
        x2 = self._anim_pos
        self.progress_bar.delete("all")
      
        self.progress_bar.create_rectangle(0, 1, w, 3, fill=BG, outline="")
        
        self.progress_bar.create_rectangle(x1, 0, x2, 4,
                                            fill=ACCENT, outline="")
        self.root.after(16, self._animate_progress)

    def start_progress(self):
        self._updating = True
        self.status_label.config(text="● Updating...", fg=YELLOW)
        self._anim_pos = 0
        self._animate_progress()

    def stop_progress(self, success: bool = True):
        self._updating = False
        if success:
            self.status_label.config(text="● Update", fg=GREEN)
          
            w = self.progress_bar.winfo_width()
            self.progress_bar.delete("all")
            self.progress_bar.create_rectangle(0, 0, w, 4,
                                                fill=GREEN, outline="")
        else:
            self.status_label.config(text="● Error", fg=RED)

   
    def get_remote_sha(self):
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/commits/{BRANCH}"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.json()["sha"]
        except Exception as e:
            self.log_print(f"Unable to join/contact GitHub: {e}", "error")
            return None

    def get_local_sha(self):
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE) as f:
                return f.read().strip()
        return None

    def save_sha(self, sha):
        with open(VERSION_FILE, "w") as f:
            f.write(sha)

    def pull_updates(self):
        result = subprocess.run(
            ["git", "pull", "origin", BRANCH],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            for line in result.stdout.strip().splitlines():
                self.log_print(line, "accent")
            return True
        else:
            for line in result.stderr.strip().splitlines():
                self.log_print(line, "error")
            return False

    def update_loop(self):
        while True:
            self.log_print("Check for updates...", "dim")
            remote = self.get_remote_sha()
            local  = self.get_local_sha()

            if remote is None:
                self.log_print("Retry in 20s. Warning! This value may be subject to modification. If you are the dev, please check the 'updater_ui.py' code. Or just verify if got a change in the name of repo/user/branch.", "warning")
            elif remote == local:
                self.log_print(
                    f"Any updates. (SHA: {remote[:7]})", "success")
            else:
                self.log_print(
                    f"New commit detected! ({remote[:7]})", "warning")
                self.root.after(0, self.start_progress)
                ok = self.pull_updates()
                if ok:
                    self.save_sha(remote)
                    self.log_print("Update successful ✓", "success")
                    self.root.after(0, lambda: self.stop_progress(True))
                    time.sleep(2)
                    self.log_print("Reboot of MIKO-AI...", "accent")
                    time.sleep(1)
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                else:
                    self.log_print("Update failure.", "error")
                    self.root.after(0, lambda: self.stop_progress(False))

            time.sleep(CHECK_INTERVAL)

    def run(self):
        self.log_print("MIKO-AI Updater starter.", "accent")
        self.log_print(f"Repo watched: {GITHUB_USER}/{GITHUB_REPO} ({BRANCH})", "dim")
        t = threading.Thread(target=self.update_loop, daemon=True)
        t.start()
        self.root.mainloop()


if __name__ == "__main__":
    UpdaterWindow().run()