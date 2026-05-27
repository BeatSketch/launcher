from util.dtype import BeatSketchBlock
from util.map.beatmap import BeatMap
from util.map.dtype.beatmap import BeatMapColorNote, CutDirection, SaberHand
from util.map.dtype.info import DifficultyLevels
from util.map.info import BeatSaberInfoFile
import shutil
import re


class BeatSaberMap:
    _info: BeatSaberInfoFile
    _maps: dict[str, BeatMap]
    _out_dir: str
    _bpm: float
    _savable: bool

    def __init__(
        self,
        folder: str,
        audio_file: str,
        cover_file: str,
        song_name: str,
        song_subtitle: str,
        song_artist: str,
        bpm: float,
        duration: int,
    ):
        """Create a new map.
        The provided folder path needs to exist. The existance is not checked until an attempt
        to write to it is made

        Args:
            folder: The folder to save the map to
            audio_file: The path to the audio file
            song_name: The name of the song
            song_subtitle: Subtitle of the song
            song_artist: The artist / composer of the song
            bpm: The BPM of the song
            duration: The duration of the song
        """
        # TODO: Can theoretically get duration from the VR app
        self._out_dir = folder
        self._maps = {}
        self._bpm = bpm

        # Copy over the audio file
        if folder == "":
            self._info = BeatSaberInfoFile(
                song_name, song_subtitle, song_artist, bpm, duration, "song.ogg"
            )
            self._savable = False
        else:
            self._savable = True
            filetype = audio_file.split(".")[-1]
            try:
                shutil.copy(audio_file, folder + "/song." + filetype)
            except FileNotFoundError:
                print("Failed to copy song. File not found")
                self._savable = False

            # Copy over the cover file
            try:
                cover_ft = cover_file.split(".")[-1]
                shutil.copy(cover_file, folder + "/cover." + cover_ft)
            except FileNotFoundError:
                print("Failed to copy cover. File not found")

            self._info = BeatSaberInfoFile(
                song_name, song_subtitle, song_artist, bpm, duration, "song." + filetype
            )

    def _pathify_name(self, name: str) -> str:
        path = ""
        regex = re.compile("[a-zA-Z]")
        regex.split(name)
        capitalize_next = True
        for letter in name:
            if regex.match(letter):
                # A letter
                if capitalize_next:
                    path += letter.capitalize()
                    capitalize_next = False
                else:
                    path += letter
            else:
                capitalize_next = True

        return path

    def save(self):
        """Save the map to the configured folder"""
        if self._out_dir == "":
            print("SAVE FAILED. Dir name invalid")
            return
        self._info.save(self._out_dir)
        for name in self._maps:
            self._maps[name].save(
                self._out_dir + "/" + self._pathify_name(name) + ".dat"
            )

    def add_difficulty(
        self, name: str, difficulty: DifficultyLevels, njs: float, mapper: str
    ):
        """Add a new beatmap / difficulty to the map

        Args:
            name: The name of the beatmap
            difficulty: The difficulty the map is going to be (such as Expert+)
            njs: The note jump speed
        """
        self._info.add_beatmap(name, difficulty, njs, mapper)
        self._maps[name] = BeatMap(self._bpm)

    def add_blocks_to_beatmap_from_real_type(
        self, beatmap: str, blocks: list[BeatMapColorNote]
    ):
        """Add a list of blocks, already in the correct format

        Args:
            beatmap: The beatmap to add to
            blocks: The blocks to add
        """
        for block in blocks:
            self._maps[beatmap].add_block_from_real_type(block)

    def add_blocks_to_beatmap_from_internal_type(
        self, beatmap: str, blocks: list[BeatSketchBlock]
    ):
        """Add a list of internal Block data types. They are automatically converted to the beatmap format.

        Args:
            beatmap: The beatmap to add to
            blocks: A list of blocks to add
        """
        for block in blocks:
            self._maps[beatmap].add_block_from_internal_block_type(block)

    def add_block_to_beatmap(
        self,
        beatmap: str,
        beat: float,
        x: int,
        y: int,
        hand: SaberHand,
        direction: CutDirection,
    ):
        """Add a block to the beatmap

        Args:
            beatmap: The beatmap to add it to
            beat: The beat at which this block is placed
            x: The lane of the block
            y: The layer of the block
            hand: The hand that this block is for
            direction: The cut direction for the block
        """
        self._maps[beatmap].add_block(beat, x, y, hand, direction)

    def remove_blocks_from_beatmap(self, beatmap: str, blocks: list[int]):
        """Remove the blocsk from the beatmap by their index

        Args:
            beatmap: The name of the beatmap to remove from
            blocks: List of block indices to remove
        """
        for offset, block in enumerate(blocks):
            self._maps[beatmap].remove_block(block - offset)

    def remove_blocks_from_beatmap_by_time(
        self, beatmap: str, start: float, end: float
    ):
        """Remove all blocks in the time frame specified

        Args:
            beatmap: The name of the beatmap to remove it from
            start: The start of the time interval, in beats
            end: The end of the time interval, in beats
        """
        offset = 0
        for idx, block in enumerate(self.get_blocks(beatmap)):
            if block["b"] >= start and block["b"] < end:
                self._maps[beatmap].remove_block(idx - offset)
                offset += 1

    def get_blocks(self, beatmap: str):
        """Get all blocks of the beatmap

        Args:
            beatmap: The beatmap to retrieve it for

        Returns:
            A list of blocks
        """
        return self._maps[beatmap].get_blocks()

    def list_beatmaps(self) -> list[str]:
        """List all the beatmaps for the current map

        Returns:
            A list of the beatmap names
        """
        maps: list[str] = []
        for map in self._maps.keys():
            maps.append(map)
        return maps

    def _get_idx_from_name(self, beatmap_name: str) -> int:
        return self.list_beatmaps().index(beatmap_name)

    def get_beatmap_difficulty(self, beatmap_name: str) -> DifficultyLevels:
        return self._info.get_difficulty(self._get_idx_from_name(beatmap_name))

    def list_beatmaps_with_difficulties(self) -> list[tuple[str, str]]:
        maps: list[tuple[str, str]] = []
        for map in self._maps.keys():
            maps.append((map, self.get_beatmap_difficulty(map)))

        return maps

    def get_bpm(self) -> float:
        return self._bpm

    def get_njs(self, beatmap_name: str) -> float:
        return self._info.get_njs(self._get_idx_from_name(beatmap_name))

    def get_audio_file(self) -> str:
        return self._out_dir + "/" + self._info.get_audio_file()


# Used to load existing maps
class ExistingBeatSaberMap(BeatSaberMap):
    def __init__(self):
        pass
