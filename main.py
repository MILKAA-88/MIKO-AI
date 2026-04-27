import threading
import sys
from start import show_boot_screen
from updater_ui import show_updater
from content import show_content

def import_modules():
    pass  

if __name__ == "__main__":
    skip_boot = "--skip-boot" in sys.argv

    thread = threading.Thread(target=import_modules)
    thread.start()

    if not skip_boot:
        show_boot_screen()

    thread.join()
    show_updater()
    show_content() 