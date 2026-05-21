from ml.dtype import MODELS
from util.ipc import BeatSketchVRApplication
from util.ipc.decode import BeatSketchBlock, BeatSketchVRData
import ml
import multiprocessing as mp


class VRDataStorage:
    def __init__(self) -> None:
        self._data: list[BeatSketchVRData] = []

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


def send_data(com: BeatSketchVRApplication, data: list[BeatSketchBlock]):
    # TODO: Possibly need to change this a bit?
    com.send_text("data:blocks")
    com.send_json(data)


class DataProcessing:
    def __init__(self, data: VRDataStorage, bpm: int, njs: float, model: MODELS):
        self._queue = mp.Queue()
        self._proc = _ProcessingProcess(data, bpm, njs, model, self._queue)
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
        self, data: VRDataStorage, bpm: int, njs: float, model: MODELS, queue: mp.Queue
    ) -> None:
        self._data: VRDataStorage = data
        self._bpm: int = bpm
        self._njs: float = njs
        self._model: MODELS = model
        self._queue = queue
        super().__init__()

    def run(self):
        self._queue.put(
            ml.process(self._data.get_data(), self._bpm, self._njs, self._model)
        )
