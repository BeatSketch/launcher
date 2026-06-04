from typing import Iterable
from map_handler.dtype import BeatSketchBlock, BeatSketchVRData


class VRDataStorage:
    def __init__(self) -> None:
        self._data: list[BeatSketchVRData] = []
        self._blocks: list[BeatSketchBlock] = []
        self._modified: bool = False

    def add_data(self, data: BeatSketchVRData):
        # Only add if playing
        if not data["paused"]:
            self._data.append(data)
            self._modified = True
        # TODO: Jump back support (i.e. partial re-recording)...
        # Also: consider how to remove blocks from the Beatmap object

    def get_data_point_count(self) -> int:
        return len(self._data)

    def get_data(self) -> list[BeatSketchVRData]:
        return self._data

    def add_blocks(self, blocks: list[BeatSketchBlock]):
        self._blocks += blocks
        self._modified = False
        self.clear_tracking()

    def clear_tracking(self):
        self._data = []

    def remove_blocks_by_idx(self, idxs: Iterable[int]):
        offset = 0
        for idx in idxs:
            self._blocks.remove(self._blocks[idx])
            offset += 1

    def get_is_modified(self):
        return self._modified

    def get_blocks(self):
        return self._blocks

    def remove_blocks_in_range(self, a: int, b: int):
        """Remove blocks in index range [a, b[ (b not inclusive)

        Args:
            a: Start of the interval
            b: End of the interval (not inclusive)
        """
        self.remove_blocks_by_idx(range(a, b))
