from time import time
from PyQt6.QtCore import QThread, pyqtSignal
from ml.dtype import MODELS
from util.ipc import BeatSketchVRApplication
from util.subprocess import processing


class BeatSketchVRAppRunner(QThread):
    # NOTE: can add more signals here if we want to display more details in the launcher
    exit_code = pyqtSignal(int)
    launch_success = pyqtSignal(bool)
    _com: BeatSketchVRApplication | None

    def __init__(self, args: list[str], bpm: int, njs: float, model: MODELS) -> None:
        super().__init__()
        self._args = args
        self._njs = njs
        self._bpm = bpm
        self._model: MODELS = model

    def __del__(self) -> None:
        if self._com:
            self._com.stop()

    def run(self) -> None:
        # Launch the VR application
        self._com = BeatSketchVRApplication(self._args + ["launcher=true"])
        if not self._com.get_alive():
            self.exit_code.emit(self._com.get_status_code())
            exit(255)

        # Initialize processing utils
        processor = processing.VRDataStorage()
        start_time = time()
        data_processing: processing.DataProcessing | None = None
        self.launch_success.emit(True)

        # Read data from process
        while True:
            data = self._com.get_data()

            # Handle the data
            if isinstance(data, dict):
                processor.add_data(self._com.parse_single_tracking_data_frame(data))
            elif data == "proc:has-quit":
                break
            elif data.strip() == "proc:do-processing":
                print(" ==> Starting processing")
                data_processing = processing.DataProcessing(
                    processor, self._bpm, self._njs, self._model
                )
            # TODO: Instruction to jump back to earlier time (maybe not explicitly needed)

            # Send data to VR
            if data_processing and data_processing.is_complete():
                # TODO: Map stiching, for when processing done mid-map, or jumping back
                self._com.send_blocks(data_processing.get_data())
                data_processing = None

        # After VR process exit, process the full map
        print(
            "\n==> Recorded",
            processor.get_data_point_count(),
            "data points in",
            time() - start_time,
            "s\n",
        )
        processed = processing.DataProcessing(
            processor, self._bpm, self._njs, self._model
        ).await_completion()
        print(processed)

        # TODO: Save the map
        if self._com.get_status_code() != 0:
            self.exit_code.emit()
            exit(self._com.get_status_code())
