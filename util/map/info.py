from util.map.dtype.info import DifficultyLevels, DifficultyLevelsConversion, InfoFile
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
        mapper: str,
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
            "_version": "2.0.0",
            "_difficultyBeatmapSets": [
                {"_beatmapCharacteristicName": "Standard", "_difficultyBeatmaps": []}
            ],
            "_songName": name,
            "_songAuthorName": author,
            "_songSubName": subtitle,
            "_levelAuthorName": "BeatSketch," + mapper,
            "_coverImageFilename": cover_file,
            "_beatsPerMinute": bpm,
            "_environmentName": "DefaultEnvironment",
            "_previewDuration": song_duration - 20,
            "_previewStartTime": 20,
            "_songFilename": audio_file,
        }

    def save(self, dir: str):
        """Save the info file to the specified directory

        Args:
            dir: The directory to save to
        """
        with open(dir + "/Info.dat", "w") as file:
            file.write(json.dumps(self._data))

    def add_beatmap(self, name: str, difficulty: DifficultyLevels, njs: float):
        """Add a beatmap, i.e. difficulty

        Args:
            name: The name of the map (will be the filename)
            difficulty: the difficulty level such as Expert+
            njs: The NoteJumpSpeed
            njs_offset: The NoteJumpSpeed Offset (typically 0)
        """
        self._data["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"].append(
            {
                "_beatmapFilename": name,
                "_difficulty": difficulty,
                "_difficultyRank": DifficultyLevelsConversion[difficulty],
                "_noteJumpMovementSpeed": njs,
                "_noteJumpStartBeatOffset": 0,
            }
        )

    def set_duration(self, duration: float):
        self._data["audio"]["songDuration"] = duration
        self._data["audio"]["previewDuration"] = int(
            duration - self._data["audio"]["previewStartTime"]
        )

    def get_njs(self, beatmap_idx: int):
        return self._data["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"][
            beatmap_idx
        ]["_noteJumpMovementSpeed"]

    def get_difficulty(self, beatmap_idx: int) -> DifficultyLevels:
        return self._data["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"][
            beatmap_idx
        ]["_difficulty"]

    def get_audio_file(self):
        return self._data["_songFilename"]
