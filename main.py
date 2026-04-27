# main.py
import sys
from display.start import show_boot_screen
from display.loading import show_loading
from display.updater_ui import show_updater
from display.content import show_content

if __name__ == "__main__":
    skip_boot = "--skip-boot" in sys.argv
    if not skip_boot:
        show_boot_screen()
    show_loading()
    show_updater()
    show_content()