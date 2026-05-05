from typing import Any, TypedDict
from util.ipc.ipc import BeatSketchInstance
import json
import numpy as np

# import quaternion as quat


class BeatSketchTrackedItemData(TypedDict):
    timestamp: int  # TODO: Possibly is float
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


class NoRunningBeatSketchInstanceError(Exception):
    pass


class BeatSketchInstanceDataDecoder:
    def __init__(self, args: list[str] = []) -> None:
        self._com = BeatSketchInstance(
            ["lovr", "../vr/"], ["BeatSketch.exe"], args
        )
        self._com.await_launch("[BeatSketch] IPC INIT COMPLETE")
        self._alive = True

    def get_data(self) -> dict | str:
        if not self._alive:
            raise NoRunningBeatSketchInstanceError()

        data = self._com.read()
        if data[0:5] == "json:":
            return json.loads(data[5:])
        elif data == "proc:has-quit":
            self._alive = False
        return data

    def parse_data(self, data: dict) -> BeatSketchVRData:
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
        self._com.write("json:" + json.dumps(data))

    def send_text(self, data: str) -> None:
        self._com.write("str:" + data)
