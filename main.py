import sys
import subprocess

def run_step(step):
    result = subprocess.run(
        [sys.executable, __file__, f"--step={step}"],
        check=False
    )
    return result.returncode

if __name__ == "__main__":
    args = sys.argv

    if "--step=boot" in args:
        from display.check import root
        from display.check import animate
        root.after(5000, animate)
        root.mainloop()

    elif "--step=loading" in args:
        from display.loading import show_loading
        show_loading()

    elif "--step=updater" in args:
        from display.updater_ui import show_updater
        show_updater()

    elif "--step=content" in args:
        from display.content import show_content
        show_content()

    else:
        skip_boot = "--skip-boot" in args
        if not skip_boot:
            run_step("boot")
        run_step("loading")
        run_step("updater")
        run_step("content")