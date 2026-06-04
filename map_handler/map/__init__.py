import os
from gui.elements import dialog
from map_handler.dtype import BeatSketchSelectedFileList
from map_handler.map.map import BeatSaberMap
from map_handler.map.dtype.info import DifficultyLevels


def _default_map():
    return BeatSaberMap(
        "",
        "",
        "",
        "Test",
        "",
        "Janis Hutz",
        "",
        150,
        150,
    )


global selected_difficulty
selected_difficulty = ""

global map
map = _default_map()


def get_map():
    return map


def new_map(
    song_name: str,
    song_artist: str,
    bpm: str,
    mapper: str,
    files: BeatSketchSelectedFileList,
    testing_mode: bool = False,
) -> bool:
    global map
    if testing_mode:
        map = _default_map()
        return True

    if files["song"] == "" or bpm == "":
        dialog.open_msg_dialog(
            "Song file and/or BPM are missing", title="Missing configuration"
        )
        return False

    try:
        float(bpm)
    except ValueError:
        dialog.open_msg_dialog(
            "BPM does not contain a valid input", title="Invalid configuration"
        )
        return False

    if not os.access(files["song"], os.R_OK):
        dialog.open_msg_dialog(
            "Song file is nonexistent or don't have read access",
            title="Invalid configuration",
        )
        return False

    if files["save"] == "":
        dialog.open_msg_dialog(
            "No map output folder selected", title="Missing configuration"
        )
        return False

    if not os.access(files["save"], os.R_OK):
        dialog.open_msg_dialog(
            "Map output folder does not exist",
            title="Invalid configuration",
        )
        return False

    if (
        files["cover"] == ""
        or files["save"] == ""
        or song_name == ""
        or song_artist == ""
    ):
        # TODO: Err msg, same checks also for other params
        # TODO: More elaborate checks
        print("Missing config, non-critical for now")

    # TODO: Retrieve the duration somehow (optinally can set that after launch of VR)
    duration = 150
    map = BeatSaberMap(files["save"], files["song"], files["cover"], song_name, "", song_artist, mapper, float(bpm), duration)
    return True


def new_difficulty(
    beatmap_name: str,
    difficulty: DifficultyLevels,
    njs: str,
    testing_mode: bool = False,
) -> bool:
    if testing_mode:
        map.add_difficulty("test", "Easy", 10)
        return True

    if njs == "" or beatmap_name == "":
        dialog.open_msg_dialog(
            "NJS and/or beatmap name are missing", title="Missing configuration"
        )
        return False

    try:
        float(njs)
    except ValueError:
        dialog.open_msg_dialog(
            "NJS does not contain a valid input", title="Invalid configuration"
        )
        return False

    map.add_difficulty(beatmap_name, difficulty, float(njs))
    return True


def set_selected_difficulty(name: str):
    global selected_difficulty
    selected_difficulty = name


def get_selected_difficulty():
    return selected_difficulty
