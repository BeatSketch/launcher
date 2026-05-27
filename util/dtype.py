from typing import TypedDict
import numpy as np
from util.map.dtype.beatmap import CutDirection, SaberHand


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
