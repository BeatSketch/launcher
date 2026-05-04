from util.map.dtype.info import DifficultyLevels, InfoFile
import json


class BeatSaberInfoFile:
    _data: InfoFile

    def __init__(
        self,
        name: str,
        subtitle: str,
        author: str,
        bpm: int,
        audio_file: str,
        song_duration: int,
        cover_file: str = "cover.png",
    ) -> None:
        self._data = {
            "version": "4.0.0",
            "difficultyBeatmaps": [],
            "song": {"title": name, "author": author, "subtitle": subtitle},
            "audio": {
                "songFilename": audio_file,
                "audioDataFilename": "BPMInfo.dat",
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

    def save(self, dir):
        with open(dir + "/Info.dat", "w") as file:
            file.write(json.dumps(self._data))

    def add_beatmap(self, difficulty: DifficultyLevels, njs: int, njs_offset: int):
        self._data["difficultyBeatmaps"].append(
            {
                "beatmapAuthors": {"mappers": ["BeatSketch"], "lighters": []},
                "beatmapDataFilename": difficulty + ".dat",
                "characteristic": "Standard",
                "difficulty": difficulty,
                "environmentNameIdx": 0,
                "lightShowDataFilename": "Lightshow.dat",
                "beatmapColorSchemeIdx": -1,
                "noteJumpMovementSpeed": njs,
                "noteJumpStartBeatOffset": njs_offset,
            }
        )
