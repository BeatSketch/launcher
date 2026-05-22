from gui.elements import dialog
import colorama
import platform

from ml.dtype import MODELS
from util.map import BeatSaberMap
from util.subprocess.runner import BeatSketchVRAppRunner
from util.subprocess.util import wayland_checks as _wayland_checks

global proc
proc: None | BeatSketchVRAppRunner = None


def start_vr_app(
    args: list[str],
    map: BeatSaberMap,
    beatmap_name: str,
    model: MODELS,
    debug: bool = False,
    dev_mode: bool = False,
) -> tuple[bool, BeatSketchVRAppRunner | None]:
    """Start the VR Application. Automatically manages the process.
    Any arguments passed should be of form key=value since this is the format
    the VR application uses, but this is not enforced

    Args:
        args: Arguments to pass to the VR application.

    Returns:
        A tuple of launch status and the process. The latter can be used to
        attach to pyqt signals to update the UI.
    """
    global proc
    if proc and proc.isRunning():
        return False, proc

    if not _wayland_checks() and platform.system() == "Linux":
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

    proc = BeatSketchVRAppRunner(args, map, beatmap_name, model, debug, dev_mode)
    proc.start()

    return True, proc
