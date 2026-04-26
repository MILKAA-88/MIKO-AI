import threading
from updater_ui import UpdaterWindow

def launch_updater():
    UpdaterWindow().run()

if __name__ == "__main__":
    threading.Thread(target=launch_updater, daemon=True).start()