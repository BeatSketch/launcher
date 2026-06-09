from typing import TypedDict

from map_handler.map.dtype.info import DifficultyLevels


class BeatSketchParsingBeatMapDifficultyData(TypedDict):
    njs: float
    difficulty: DifficultyLevels
    file: str
