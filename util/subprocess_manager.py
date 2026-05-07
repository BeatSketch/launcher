from PyQt6.QtCore import QThread, pyqtSignal
from util.ipc import BeatSketchVRApplication
from gui.elements import dialog
from util.ipc.decode import BeatSketchVRData
import colorama
import datetime
import multiprocessing as mp
import os
import platform
import subprocess as sp
import time

global proc
proc: None | mp.Process = None


class StartupHandlerThread(QThread):
    result_ready = pyqtSignal(int)

    def __init__(self) -> None:
        self._proc: None | mp.Process = None
        super().__init__()

    def run(self) -> None:
        print("Launching monitoring process")
        if not self._proc:
            return
        for _ in range(10):
            time.sleep(2)
            if not self._proc.is_alive():
                self.result_ready.emit(self._proc.exitcode)
                return

    def set_proc(self, proc: mp.Process):
        self._proc = proc


def _wayland_checks() -> bool:
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


def start_vr_app(args: list[str], helper_thread: StartupHandlerThread):
    global proc
    if proc and proc.is_alive():
        return False

    if not _wayland_checks():
        dialog.open_msg_dialog(
            "Gamescope is not installed. Please install it using your distribution's package manager",
            title="Launching VR Application failed",
        )
        return False

    print(
        colorama.Fore.GREEN
        + colorama.Style.DIM
        + "==> Pre-Launch checks passed, launching VR app"
        + colorama.Style.RESET_ALL
    )
    proc = mp.Process(target=_run, args=(args,))
    proc.start()
    helper_thread.set_proc(proc)
    helper_thread.start()
    return True


def _run(args: list[str]):
    com = BeatSketchVRApplication(args)
    if not com.get_alive():
        exit(255)
    all_data: list[BeatSketchVRData] = []
    start_time = datetime.datetime.now().timestamp()
    while True:
        data = com.get_data()
        if isinstance(data, dict):
            # TODO: send to processing (or do processing here, but that is likely not *that* smart of an idea)
            # because likely resource intensive
            # CONSIDERATION: Do processing only once map is fully played or user hits pause
            # THEN: Send data back to the VR application so we can move back to adjust?
            all_data.append(com.parse_data(data))
        elif data == "proc:has-quit":
            print("\n\nEXITING SUBPROCESS\n\n")
            time_diff = datetime.datetime.now().timestamp() - start_time
            print("Recorded", len(all_data), "data points in", time_diff, "s")
            print("-> Thus", len(all_data) / time_diff, "data points per second")
            if com.get_status_code() != 0:
                exit(com.get_status_code())
            return
        # TODO: Instruction to jump back to earlier time (maybe not explicitly needed)
