import colorama
import multiprocessing as mp
import os
import platform
import subprocess as sp
from util.ipc import BeatSketchVRApplication
from gui.elements import dialog

global proc
proc: None | mp.Process = None


def _wayland_checks() -> bool:
    if platform.system() == "Linux":
        # Detect Wayland
        if (
            os.getenv("XDG_BACKEND") == "wayland"
            or os.getenv("XDG_SESSION_TYPE") == "wayland"
        ):
            status = sp.run(["which", "gamescope"], capture_output=True, text=True).stdout
            return status != ""
    return False


def start_vr_app(args: list[str]):
    global proc
    if proc and proc.is_alive():
        return False

    if not _wayland_checks():
        dialog.open_msg_dialog(
            "Gamescope is not installed. Please install it using your distribution's package manager",
            title="Launching VR Application failed",
        )
        return False

    print(colorama.Fore.GREEN + colorama.Style.DIM + "==> Pre-Launch checks passed, launching VR app" + colorama.Style.RESET_ALL)
    proc = mp.Process(target=_run, args=(args,))
    proc.start()

    return True


def _run(args: list[str]):
    com = BeatSketchVRApplication(args)
    while True:
        data = com.get_data()
        if isinstance(data, dict):
            print(com.parse_data(data))
        elif data == "proc:has-quit":
            print("\n\nEXITING SUBPROCESS\n\n")
            return
        # TODO: Instruction to jump back to earlier time (maybe not explicitly needed)
