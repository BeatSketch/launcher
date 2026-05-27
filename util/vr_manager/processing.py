from typing import Iterable
from ml.dtype import MODELS
from util.dtype import BeatSketchBlock, BeatSketchVRData
import ml
import multiprocessing as mp


class VRDataStorage:
    def __init__(self) -> None:
        self._data: list[BeatSketchVRData] = []
        self._blocks: list[BeatSketchBlock] = []

    def add_data(self, data: BeatSketchVRData):
        # Only add if playing
        if not data["paused"]:
            self._data.append(data)
        # TODO: Jump back support (i.e. partial re-recording)...
        # probably just going to destroy this object and recreate
        # -> Possible issues from that: processing pipeline a bit harder
        # Also: consider how to remove blocks from the Beatmap object

    def get_data_point_count(self) -> int:
        return len(self._data)

    def get_data(self) -> list[BeatSketchVRData]:
        return self._data

    def add_blocks(self, blocks: list[BeatSketchBlock]):
        self._blocks += blocks

    def remove_blocks_by_idx(self, idxs: Iterable[int]):
        offset = 0
        for idx in idxs:
            self._blocks.remove(self._blocks[idx])
            offset += 1

    def remove_blocks_in_range(self, a: int, b: int):
        """Remove blocks in index range [a, b[ (b not inclusive)

        Args:
            a: Start of the interval
            b: End of the interval (not inclusive)
        """
        self.remove_blocks_by_idx(range(a, b))


class BeatSketchProcessingManager:
    def __init__(
        self,
        data: VRDataStorage,
        bpm: int,
        njs: float,
        model: MODELS,
        dev_mode: bool = False,
    ):
        self._queue = mp.Queue()
        self._proc = _ProcessingProcess(data, bpm, njs, model, self._queue, dev_mode)
        self._proc.start()

    def is_complete(self) -> bool:
        return not self._proc.is_alive()

    def get_data(self) -> list[BeatSketchBlock]:
        return self._queue.get() if not self._queue.empty() else []

    def await_completion(self) -> list[BeatSketchBlock]:
        self._proc.join()
        return self.get_data()


class _ProcessingProcess(mp.Process):
    def __init__(
        self,
        data: VRDataStorage,
        bpm: int,
        njs: float,
        model: MODELS,
        queue: mp.Queue,
        dev_mode: bool = False,
    ) -> None:
        self._data: VRDataStorage = data
        self._bpm: int = bpm
        self._njs: float = njs
        self._model: MODELS = model
        self._queue = queue
        self._dev_mode = dev_mode
        super().__init__()

    def run(self):
        self._queue.put(
            ml.process(
                self._data.get_data(), self._bpm, self._njs, self._model, self._dev_mode
            )
        )
