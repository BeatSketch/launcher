from typing import TypedDict
import numpy as np
from map_handler.map.dtype.beatmap import CutDirection, SaberHand

class BeatSketchSelectedFileList(TypedDict):
    song: str
    save: str
    cover: str


class BeatSketchTrackedItemData(TypedDict):
    timestamp: float
    pos: np.ndarray
    direction: np.ndarray
    quat: np.ndarray  # TODO: Use the quaternion package instead?
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
