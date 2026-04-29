from typing import Any
from util.ipc.ipc import BeatSketchInstance
import json


class NoRunningBeatSketchInstanceError(Exception):
    pass


class BeatSketchInstanceDataDecoder:
    def __init__(self, args: list[str] = []) -> None:
        self._com = BeatSketchInstance(["lovr", "../BeatSketch/"], ["BeatSketch.exe"], args)
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

    def send_json(self, data: dict | list[Any]) -> None:
        self._com.write("json:" + json.dumps(data))

    def send_text(self, data: str) -> None:
        self._com.write("str:" + data)
