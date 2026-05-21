import os
import platform
import subprocess as sp


def wayland_checks() -> bool:
    if platform.system() == "Linux":
        # Detect Wayland
        if (
            os.getenv("XDG_BACKEND") == "wayland"
            or os.getenv("XDG_SESSION_TYPE") == "wayland"
        ):
            status = sp.run(
                ["which", "gamescope"], capture_output=True, text=True
            ).stdout
            return status != ""
    return False
