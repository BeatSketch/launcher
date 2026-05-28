from util.map.dtype.info import DifficultyLevels, InfoFile
import json


class BeatSaberInfoFile:
    _data: InfoFile

    def __init__(
        self,
        name: str,
        subtitle: str,
        author: str,
        bpm: float,
        song_duration: int,
        audio_file: str = "song.ogg",
        cover_file: str = "cover.png",
    ) -> None:
        """Create a new Info File

        Args:
            name: Name of the song
            subtitle: Subtitle of the song
            author: Author / Artist of the song
            bpm: The BPM of the song
            song_duration: The duration of the song
            audio_file: The filename of the audio file (optional, defaults to song.ogg)
            cover_file: The cover art file (optional, defaults to cover.png)
        """
        self._data = {
            "version": "4.0.0",
            "difficultyBeatmaps": [],
            "song": {"title": name, "author": author, "subtitle": subtitle},
            "audio": {
                "songFilename": audio_file,
                "bpm": bpm,
                "lufs": 0,
                "previewStartTime": 20,
                "previewDuration": song_duration - 20,
                "songDuration": song_duration,
            },
            "coverImageFilename": cover_file,
            "environmentNames": ["DefaultEnvironment"],
            "songPreviewFilename": audio_file,
        }

    def save(self, dir: str):
        """Save the info file to the specified directory

        Args:
            dir: The directory to save to
        """
        with open(dir + "/Info.dat", "w") as file:
            file.write(json.dumps(self._data))

    def add_beatmap(
        self, name: str, difficulty: DifficultyLevels, njs: float, mapper: str
    ):
        """Add a beatmap, i.e. difficulty

        Args:
            name: The name of the map (will be the filename)
            difficulty: the difficulty level such as Expert+
            njs: The NoteJumpSpeed
            njs_offset: The NoteJumpSpeed Offset (typically 0)
        """
        self._data["difficultyBeatmaps"].append(
            {
                "beatmapAuthors": {"mappers": ["BeatSketch", mapper], "lighters": []},
                "beatmapDataFilename": name + ".dat",
                "characteristic": "Standard",
                "difficulty": difficulty,
                "environmentNameIdx": 0,
                "lightShowDataFilename": "Lightshow.dat",
                "beatmapColorSchemeIdx": -1,
                "noteJumpMovementSpeed": njs,
                "noteJumpStartBeatOffset": 0,
            }
        )

    def get_njs(self, beatmap_idx: int):
        return self._data["difficultyBeatmaps"][beatmap_idx]["noteJumpMovementSpeed"]

    def get_difficulty(self, beatmap_idx: int) -> DifficultyLevels:
        return self._data["difficultyBeatmaps"][beatmap_idx]["difficulty"]

    def get_audio_file(self):
        return self._data["audio"]["songFilename"]
