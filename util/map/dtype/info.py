from typing import Literal, Optional, TypedDict

DifficultyLevels = Literal["Easy", "Normal", "Hard", "Expert", "Expert+"]


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

    version: str
    difficultyBeatmaps: list[BeatMapDifficulty]
    song: BeatMapSongDetails
    audio: BeatMapAudioDetails
    songPreviewFilename: str
    coverImageFilename: str
    environmentNames: list[str]


class BeatMapSongDetails(TypedDict):
    """Details for the song (name and author)

    Attributes:
        title: The song name / title
        subtitle: A subtitle for the song
        author: The artist(s) for the song
    """

    title: str
    subtitle: Optional[str]
    author: str


class BeatMapAudioDetails(TypedDict):
    """Details for the audio file and pre-caching for the UI

    Attributes:
        songFilename: The file name for the audio file to use
        songDuration: The duration of the song
        audioDataFilename: The file containing audio data
        bpm: The song bpm (default or most common, displayed in UI)
        lufs: Loudness of the song (defaults to 0 for no change)
        previewStartTime: The point in the song from which to start the preview
        previewDuration: The duration of the audio preview played
    """

    songFilename: str
    songDuration: int
    audioDataFilename: str
    bpm: int
    lufs: int
    previewStartTime: int
    previewDuration: int


class BeatMapAuthors(TypedDict):
    """Mappers and lighters of the map

    Attributes:
        mappers: List of mappers
        lighters: List of lighters
    """

    mappers: list[str]
    lighters: list[str]


class BeatMapDifficulty(TypedDict):
    """Details for a level / difficulty

    Attributes:
        characteristic: The characteristic of the map (currently only Standard supported)
        difficulty: The difficulty of the map (e.g. Expert+)
        beatmapAuthors: The authors of the map
        environmentNameIdx: The environment index in the environments list in info
        noteJumpMovementSpeed: The Note Jump Speed
        noteJumpStartBeatOffset: NJS offset
        beatmapDataFilename: The filename of the Beatmap (default: <Difficulty>.dat)
        lightShowDataFilename: The file of the Lightshow (default: Lightshow.dat)
        beatmapColorSchemeIdx: The color scheme to use (default -1, means use default for env)
    """

    characteristic: Literal["Standard"]
    difficulty: DifficultyLevels
    beatmapAuthors: BeatMapAuthors
    environmentNameIdx: int
    noteJumpMovementSpeed: int
    noteJumpStartBeatOffset: int
    beatmapDataFilename: str
    lightShowDataFilename: str
    beatmapColorSchemeIdx: int
