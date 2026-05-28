from time import sleep, time
from PyQt6.QtCore import QThread, pyqtSignal
from ml.dtype import MODELS
from util.ipc import BeatSketchVRApplication
from util.map import BeatSaberMap
from util.vr_manager import processing


class BeatSketchVRMonitoringThread(QThread):
    # NOTE: can add more signals here if we want to display more details in the launcher
    exit_code = pyqtSignal(int)
    launch_success = pyqtSignal(bool)
    _com: BeatSketchVRApplication | None

    def __init__(
        self,
        args: list[str],
        map: BeatSaberMap,
        beatmap_name: str,
        model: MODELS,
        debug: bool = False,
        dev_mode: bool = False,
    ) -> None:
        self._args = args
        self._beatmap_name = beatmap_name
        self._njs = map.get_njs(beatmap_name)
        self._bpm = map.get_bpm()
        self._map = map
        self._beatmap_name = beatmap_name
        self._model: MODELS = model
        self._debug = debug
        self._dev_mode = dev_mode
        super().__init__()

    def __del__(self) -> None:
        if self._com:
            self._com.stop()

    def run(self) -> None:
        # Launch the VR application
        self._com = BeatSketchVRApplication(
            self._args + ["launcher=true"], dev_mode=self._dev_mode
        )
        if not self._com.get_alive():
            self.exit_code.emit(self._com.get_status_code())
            sleep(2)
            return

        # Initialize processing utils
        processor = processing.VRDataStorage()
        start_time = time()
        data_processing: processing.BeatSketchProcessingManager | None = None
        self.launch_success.emit(True)

        # Read data from process
        while True:
            data = self._com.get_data()

            # Handle the data
            if isinstance(data, dict):
                processor.add_data(self._com.parse_single_tracking_data_frame(data))
            elif data == "proc:has-quit":
                break
            elif data == "proc:do-processing":
                print("Starting processing")
                data_processing = processing.BeatSketchProcessingManager(
                    processor, self._bpm, self._njs, self._model, self._dev_mode
                )
            elif data.startswith("proc:overwrite-from:"):
                print("Overwriting song data")
                # TODO: Implement this
            elif self._debug:
                print(data)

            # Send data to VR
            if data_processing and data_processing.is_complete():
                # TODO: Map stiching, for when processing done mid-map, or jumping back, or map has existing parts
                data = data_processing.get_data()
                print("Processing complete, generated", len(data), "blocks")
                self._com.send_blocks(data)
                data_processing = None

        # After VR process exit, process the full map
        if self._debug:
            print(
                "\n==> Recorded",
                processor.get_data_point_count(),
                "data points in",
                time() - start_time,
                "s\n",
            )
        processed = processing.BeatSketchProcessingManager(
            processor, self._bpm, self._njs, self._model, self._dev_mode
        ).await_completion()
        self._map.add_blocks_to_beatmap_from_internal_type(
            self._beatmap_name, processed
        )
        self._map.save()

        if self._com.get_status_code() != 0:
            self.exit_code.emit(self._com.get_status_code())
            exit(self._com.get_status_code())
