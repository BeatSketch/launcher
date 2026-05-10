from PyQt6.QtCore import QThread, pyqtSignal
from util.ipc import BeatSketchVRApplication
from gui.elements import dialog
from util.ipc.decode import BeatSketchVRData
import colorama
import datetime
import os
import platform
import subprocess as sp

global proc
proc: None | BeatSketchVRAppRunner = None


class BeatSketchVRAppRunner(QThread):
    # NOTE: can add more signals here if we want to display more details in the launcher
    exit_code = pyqtSignal(int)
    launch_success = pyqtSignal(bool)
    _com: BeatSketchVRApplication | None

    def __init__(self, args: list[str]) -> None:
        super().__init__()
        self._args = args

    def __del__(self) -> None:
        if self._com:
            self._com.stop()

    def run(self) -> None:
        self._com = BeatSketchVRApplication(self._args)
        if not self._com.get_alive():
            self.exit_code.emit(self._com.get_status_code())
            exit(255)
        all_data: list[BeatSketchVRData] = []
        start_time = datetime.datetime.now().timestamp()
        self.launch_success.emit(True)
        # TODO: Any really performance intensive stuff
        # should happen in a separate thread for best perf
        while True:
            data = self._com.get_data()
            if isinstance(data, dict):
                # TODO: send to processing (or do processing here, but that is likely not *that* smart of an idea)
                # because likely resource intensive
                # CONSIDERATION: Do processing only once map is fully played or user hits pause
                # THEN: Send data back to the VR application so we can move back to adjust?
                all_data.append(self._com.parse_data(data))
            elif data == "proc:has-quit":
                print("\n\nEXITING SUBPROCESS\n\n")
                time_diff = datetime.datetime.now().timestamp() - start_time
                print("Recorded", len(all_data), "data points in", time_diff, "s")
                print("-> Thus", len(all_data) / time_diff, "data points per second")
                if self._com.get_status_code() != 0:
                    self.exit_code.emit()
                    exit(self._com.get_status_code())
                return
            # TODO: Instruction to jump back to earlier time (maybe not explicitly needed)


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


def start_vr_app(args: list[str]) -> tuple[bool, BeatSketchVRAppRunner | None]:
    global proc
    if proc and proc.isRunning():
        return False, proc

    if not _wayland_checks():
        dialog.open_msg_dialog(
            "Gamescope is not installed. Please install it using your distribution's package manager",
            title="Launching VR Application failed",
        )
        return False, proc

    print(
        colorama.Fore.GREEN
        + colorama.Style.DIM
        + "==> Pre-Launch checks passed, launching VR app"
        + colorama.Style.RESET_ALL
    )

    proc = BeatSketchVRAppRunner(args)
    proc.start()

    return True, proc
