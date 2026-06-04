from typing import TypedDict
from util.dtype import BeatSketchBlock
import numpy as np


class BeatSketchCleanupGroup(TypedDict):
    block: BeatSketchBlock
    tracking: list[np.ndarray]
    beat: float

class BeatSketchCleanup(TypedDict):
    left: list[BeatSketchCleanupGroup]
    right: list[BeatSketchCleanupGroup]
    bpm: float
