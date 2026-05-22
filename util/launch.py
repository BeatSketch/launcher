import os
from typing import Callable, TypedDict
from gui.elements import dialog
from util.map import BeatSaberMap
from util.map.dtype.info import DifficultyLevels
from util.subprocess import start_vr_app


class BeatSketchSelectedFileList(TypedDict):
    song: str
    save: str
    cover: str


def launch_wrapper(
    song_name: str,
    song_artist: str,
    mapper: str,
    map: BeatSaberMap,
    beatmap_name: str,
    difficulty: DifficultyLevels,
    bpm: str,
    njs: str,
    files: BeatSketchSelectedFileList,
    launch_func: Callable[[], None],
    testing_mode: bool = False,
    vr_debug: bool = False,
):
    """A convenience wrapper for the VR app launch procedure.

    Args:
        song_name: The name of the song
        song_artist: Name of the artist
        mapper: The name of the mapper
        bpm: The song's BPM
        njs: The song's Note Jump Speed
        files: The files that the user picked
        launch_func: A function to run before the launch happens
    """
    if (files["song"] == "" or bpm == "" or njs == "") and not testing_mode:
        dialog.open_msg_dialog(
            "Song file, BPM and/or NJS are missing", title="Missing configuration"
        )
        return

    if not os.access(files["song"], os.R_OK) and not testing_mode:
        dialog.open_msg_dialog(
            "Song file is nonexistent or don't have read access",
            title="Missing configuration",
        )
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

    launch_func()
    # TODO: Load rotation offsets for sabers from config
    args = [
        f'song="{files["song"]}"',
        f"bpm={bpm}",
        f"rx={0}",
        f"ry={0}",
        f"rz={0}",
        f"njs={njs}",
    ]
    if testing_mode:
        args = []
        bpm = "100"
        njs = "10"

    # Add difficulty
    # TODO: What to do for existing maps?
    map.add_difficulty(beatmap_name, difficulty, float(njs))
    status, proc = start_vr_app(args, map, beatmap_name, "testing", debug=vr_debug)
    # TODO: Change model here, or move to somewhere else, like config

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
