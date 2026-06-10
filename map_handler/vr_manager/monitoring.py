from time import sleep, time
from PyQt6.QtCore import QThread, pyqtSignal
from map_handler.ml.dtype import MODELS
from map_handler.vr_manager.ipc import BeatSketchVRApplication
from map_handler import BeatSaberMap
from map_handler.vr_manager import processing
from map_handler.vr_manager.storage import VRDataStorage


class BeatSketchVRMonitoringThread(QThread):
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
        storage = VRDataStorage(self._bpm)
        start_time = time()
        data_processing: processing.BeatSketchProcessingManager | None = None
        self.launch_success.emit(True)

        # Read data from process
        while True:
            data = self._com.get_data()

            # Handle the data
            if isinstance(data, dict):
                storage.add_data(self._com.parse_single_tracking_data_frame(data))
            elif data == "proc:has-quit":
                break
            elif data == "proc:do-processing":
                locs = storage.remove_blocks_in_recorded_time()
                self._map.remove_blocks_from_beatmap_by_time(
                    self._beatmap_name,
                    locs[0],
                    locs[1],
                )

                data_processing = processing.BeatSketchProcessingManager(
                    storage, self._bpm, self._njs, self._model, self._dev_mode
                )
            elif data.startswith("proc:overwrite"):
                storage.clear_tracking()
            elif data.startswith("proc:duration:"):
                self._map.set_duration(float(data[14:]))
            elif data == "proc:existing-blocks":
                self._com.send_blocks(
                    self._map.get_blocks_in_beatsketch_format(self._beatmap_name)
                )
            elif self._debug:
                print(data)

            # Send data to VR
            if data_processing and data_processing.is_complete():
                data = data_processing.get_data()
                print("=> Map processed")
                if self._dev_mode:
                    print("Processing complete, generated", len(data), "blocks")
                storage.add_blocks(data)
                self._com.send_blocks(data)
                data_processing = None

        if self._debug:
            print(
                "\n==> Recorded",
                storage.get_data_point_count(),
                "data points in",
                time() - start_time,
                "s\n",
            )

        # Only do processing if there is new data
        if storage.get_is_modified():
            processed = processing.BeatSketchProcessingManager(
                storage, self._bpm, self._njs, self._model, self._dev_mode
            ).await_completion()
            storage.add_blocks(processed)

        # Save the map
        self._map.add_blocks_to_beatmap_from_internal_type(
            self._beatmap_name, storage.get_blocks()
        )
        self._map.save()
        print("=> Map saved")

        if self._com.get_status_code() != 0:
            self.exit_code.emit(self._com.get_status_code())
            exit(self._com.get_status_code())
