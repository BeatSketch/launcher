from typing import cast
from util.map.beatmap import BeatMap
from util.map.info import BeatSaberInfoFile
import shutil


class BeatSaberMap:
    _info: BeatSaberInfoFile
    _maps: dict[str, BeatMap]
    _out_dir: str

    def __init__(
        self,
        folder: str,
        audio_file: str,
        song_name: str,
        song_subtitle: str,
        song_artist: str,
        bpm: int,
        duration: int,
    ):
        self._out_dir = folder
        self._maps = {}

        # Copy over the audio file
        filetype = audio_file.split(".")[-1]
        shutil.copy(audio_file, folder + "/song." + filetype)

        self._info = BeatSaberInfoFile(
            song_name, song_subtitle, song_artist, bpm, duration, "song." + filetype
        )

    def save_map(self):
        pass

    def add_difficulty(self):
        pass

    def update_beatmap(self):
        # To update the blocks
        pass

    def update_beatmap_details(self):
        # To update any config
        pass

    def list_beatmaps(self) -> list[str]:
        return cast(list[str], self._maps.keys())


# Used to load existing maps
class ExistingBeatSaberMap(BeatSaberMap):
    def __init__(self):
        pass
