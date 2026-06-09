import os
from gui.elements import dialog
from map_handler.dtype import BeatSketchSelectedFileList
from map_handler.map.load import load_map
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


def import_map(path: str) -> bool:
    """Import an existing map into BeatSketch

    Args:
        path: The path to the folder of the map

    Returns:
        True if successful, False otherwise
    """
    global map
    data = load_map(path)
    if data:
        map = data
        return True
    else:
        return False


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

    if song_name == "" or song_artist == "":
        dialog.open_msg_dialog(
            "Missing song name and/or artist",
            title="Invalid configuration",
        )
        return False

    if mapper == "":
        dialog.open_msg_dialog(
            "No mapper name set",
            title="Invalid configuration",
        )
        return False

    if files["cover"] == "":
        dialog.open_msg_dialog(
            "No song cover provided. The map can still be created without one",
            title="Incomplete configuration",
        )

    duration = 120
    map = BeatSaberMap(
        files["save"],
        files["song"],
        files["cover"],
        song_name,
        "",
        song_artist,
        mapper,
        float(bpm),
        duration,
    )
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
