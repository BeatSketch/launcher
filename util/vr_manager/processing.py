from ml.dtype import MODELS
from util.dtype import BeatSketchBlock
import ml
import multiprocessing as mp

from util.vr_manager.storage import VRDataStorage


class BeatSketchProcessingManager:
    def __init__(
        self,
        data: VRDataStorage,
        bpm: float,
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
        bpm: float,
        njs: float,
        model: MODELS,
        queue: mp.Queue,
        dev_mode: bool = False,
    ) -> None:
        self._data: VRDataStorage = data
        self._bpm: float = bpm
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
