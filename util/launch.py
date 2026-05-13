import os
from typing import Callable

from gui.elements import dialog
from util.subprocess_manager import start_vr_app


def launch_wrapper(
    song_name: str,
    song_artist: str,
    mapper: str,
    bpm: str,
    files: dict[str, str],
    launch_func: Callable[[], None],
):
    if files["song"] == "" or bpm == "":
        dialog.open_msg_dialog("Song file and/or BPM are missing", title="Missing configuration")
        return

    if not os.access(files["song"], os.R_OK):
        dialog.open_msg_dialog("Song file is nonexistent or don't have read access", title="Missing configuration")
        return

    if (
        files["cover"] == ""
        or files["save"] == ""
        or song_name == ""
        or song_artist == ""
        or mapper == ""
    ):
        # TODO: Err msg, same checks also for other params
        # TODO: More elaborate checks
        print("Missing config, non-critical for now")

    # TODO: Where to get the rotations from?
    launch_func()
    status, proc = start_vr_app(
        [f'song="{files["song"]}"', f"bpm={bpm}", f"rx={0}", f"ry={0}", f"rz={0}"]
    )

    def launch_status_handler(status: int):
        if status != 0:
            dialog.open_msg_dialog(
                "The VR Application has failed to launch. Exit code: " + str(status),
                title="Launching VR Application failed",
            )

    if proc and status:
        proc.exit_code.connect(launch_status_handler)
    else:
        launch_status_handler(254)
