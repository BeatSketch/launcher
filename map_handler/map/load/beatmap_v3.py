from map_handler.map.dtype.beatmap import BeatMapColorNote
from map_handler.map.load.dtype import BeatSketchParsingBeatMapDifficultyData
from map_handler.map.map import BeatSaberMap


def parse(
    data: dict,
    details: BeatSketchParsingBeatMapDifficultyData,
    map: BeatSaberMap,
) -> bool:
    beatmap_name = details["file"].split(".")[0]
    map.add_difficulty(beatmap_name, details["difficulty"], details["njs"])
    blocks: list[BeatMapColorNote] = []
    try:
        for block in data["colorNotes"]:
            blocks.append(
                {
                    "a": block["a"],
                    "b": block["b"],
                    "c": block["c"],
                    "d": block["d"],
                    "x": block["x"],
                    "y": block["y"],
                }
            )
    except KeyError:
        return False

    map.add_blocks_to_beatmap_from_real_type(beatmap_name, blocks)
    return True
