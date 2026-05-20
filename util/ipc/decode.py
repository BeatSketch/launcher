from typing import Any, TypedDict
from util.ipc.ipc import BeatSketchInstance
import json
import numpy as np

from util.map.dtype.beatmap import CutDirection, SaberHand

# import quaternion as quat


class BeatSketchTrackedItemData(TypedDict):
    timestamp: float
    pos: np.ndarray
    direction: np.ndarray
    quat: np.ndarray  # TODO: Use the quaternion package instead
    tip: np.ndarray
    buttons: list[str]


class BeatSketchVRData(TypedDict):
    left: BeatSketchTrackedItemData
    right: BeatSketchTrackedItemData
    head: BeatSketchTrackedItemData
    paused: bool


class BeatSketchBlock(TypedDict):
    x: int
    y: int
    orientation: CutDirection
    beat: float
    hand: SaberHand


class NoRunningBeatSketchInstanceError(Exception):
    pass


class BeatSketchInstanceDataHandler:
    def __init__(self, args: list[str] = []) -> None:
        """Initialize a new VR application

        Args:
            args: The CLI args to pass in. Typically should be list of key=val,
            because that's what the VR app uses
        """
        self._com = BeatSketchInstance(["lovr", "../vr/"], ["BeatSketch.exe"], args)
        self._alive = self._com.await_launch("[BeatSketch] IPC INIT COMPLETE")

    def get_alive(self) -> bool:
        """Check if the VR application is running

        Returns:
            True if running, False otherwise
        """
        return self._alive

    def stop(self) -> int:
        """Stop the VR application

        Returns:
            The exit code of the app
        """
        return self._com.await_close()

    def get_status_code(self) -> int:
        """Retrieve the status code

        Returns:
            The status code, if available
        """
        return self._com.get_status_code()

    def get_data(self) -> dict | str:
        """Read data from the stdout of the VR application

        Returns:
            The parsed data (if applicable) or the raw data

        Raises:
            NoRunningBeatSketchInstanceError: If no instance is running
        """
        if not self._alive:
            raise NoRunningBeatSketchInstanceError()

        data = self._com.read()
        if data[0:5] == "json:":
            return json.loads(data[5:])
        elif data == "proc:has-quit":
            self._alive = False
        return data

    def parse_single_tracking_data_frame(self, data: dict) -> BeatSketchVRData:
        """Parse the VR data into a usable format. For a single data point only

        Args:
            data: The data received

        Returns:
            The parsed data

        Raises:
            ValueError: If the passed in data is not in fact a dict
        """
        if not isinstance(type(data), dict):
            raise ValueError("Passed in data is not a dictionary")

        return {
            "left": {
                "buttons": data["left"]["buttons"],
                "pos": np.array(data["left"]["pos"]),
                "direction": np.array(data["left"]["direction"]),
                "quat": np.array(data["left"]["quat"]),
                "tip": np.array(data["left"]["tip"]),
                "timestamp": int(data["left"]["timestamp"]),
            },
            "right": {
                "buttons": data["right"]["buttons"],
                "pos": np.array(data["right"]["pos"]),
                "direction": np.array(data["right"]["direction"]),
                "quat": np.array(data["right"]["quat"]),
                "tip": np.array(data["right"]["tip"]),
                "timestamp": int(data["right"]["timestamp"]),
            },
            "head": {
                "buttons": data["head"]["buttons"],
                "pos": np.array(data["head"]["pos"]),
                "direction": np.array(data["head"]["direction"]),
                "quat": np.array(data["head"]["quat"]),
                "tip": np.array(data["head"]["tip"]),
                "timestamp": int(data["head"]["timestamp"]),
            },
            "paused": data["paused"],
        }

    def send_json(self, data: dict | list[Any]) -> None:
        """Send JSON data to the VR application

        Args:
            data: The data to send
        """
        # TODO: Probably want to use a queue here,
        # or in the abstraction to not block the VR app
        self._com.write("json:" + json.dumps(data))

    def send_blocks(self, data: list[BeatSketchBlock]) -> None:
        """Send the processed blocks back to VR

        Args:
            data: The blocks
        """
        self.send_text("proc:send-blocks")
        self.send_json(data)
        self.send_text("proc:last-instr")

    def send_text(self, data: str) -> None:
        """Send a plain instruction, of any format to VR

        Args:
            data: The data to send
        """
        self._com.write("str:" + data)
