from typing import Literal, TypedDict

DifficultyLevels = Literal["Easy", "Normal", "Hard", "Expert", "Expert+"]
DifficultyLevelsRank = Literal[1, 3, 5, 7, 9]
DifficultyLevelsConversion: dict[DifficultyLevels, DifficultyLevelsRank] = {
    "Easy": 1,
    "Normal": 3,
    "Hard": 5,
    "Expert": 7,
    "Expert+": 9,
}


class InfoFile(TypedDict):
    """Beat Saber Info file (main entrypoint for the map)

    Attributes:
        version: The InfoFile version
        difficultyBeatmaps: A list of all levels / difficulties of the map
        song: Song details
        audio: Audio details
        songPreviewFilename: Optional file for preview (default: same as song)
        coverImageFilename: The file for the cover image
        environmentNames: The environments this map uses
    """

    _version: str
    _songName: str
    _songSubName: str
    _songAuthorName: str
    _levelAuthorName: str
    _beatsPerMinute: float
    _previewStartTime: int
    _previewDuration: int
    _songFilename: str
    _coverImageFilename: str
    _environmentName: str
    # Types such as "Standard"
    _difficultyBeatmapSets: list[BeatMapDifficultySets]


class BeatMapDifficultySets(TypedDict):
    _beatmapCharacteristicName: Literal["Standard"]
    _difficultyBeatmaps: list[BeatMapDifficulty]


class BeatMapDifficulty(TypedDict):
    _difficulty: DifficultyLevels
    _beatmapFilename: str
    _difficultyRank: DifficultyLevelsRank
    _noteJumpMovementSpeed: float
    _noteJumpStartBeatOffset: float
