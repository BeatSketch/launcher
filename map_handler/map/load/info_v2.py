from typing import cast

from map_handler.map.dtype.info import (
    DifficultyLevelsConversionInverse,
    DifficultyLevelsRank,
)
from map_handler.map.load.dtype import BeatSketchParsingBeatMapDifficultyData
from map_handler.map.map import BeatSaberMap


def parse(
    data: dict, folder: str
) -> tuple[list[BeatSketchParsingBeatMapDifficultyData], BeatSaberMap | None]:
    try:
        beatmaps: list[BeatSketchParsingBeatMapDifficultyData] = []
        for diff_set in data["_difficultyBeatmapSets"]:
            try:
                if diff_set["_beatmapCharacteristicName"] == "Standard":
                    for difficulty in diff_set["_difficultyBeatmaps"]:
                        try:
                            beatmaps.append(
                                {
                                    "file": "",
                                    "difficulty": DifficultyLevelsConversionInverse[
                                        cast(
                                            DifficultyLevelsRank,
                                            int(difficulty["_difficultyRank"]),
                                        )
                                    ],
                                    "njs": float(difficulty["_noteJumpMovementSpeed"]),
                                }
                            )
                        except KeyError:
                            pass
            except KeyError:
                pass

        return beatmaps, BeatSaberMap(
            folder,
            data["_songFilename"],
            data["_coverImageFilename"],
            data["_songName"],
            data["_songSubName"],
            data["_songAuthorName"],
            data["_levelAuthorName"],
            float(data["_beatsPerMinute"]),
            200,
        )
    except KeyError:
        return [], None
