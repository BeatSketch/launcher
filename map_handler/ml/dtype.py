from typing import Literal, TypedDict
import numpy as np


class BeatSketchTrackingData(TypedDict):
    left: list[BeatSketchTrackingDataDetails]
    right: list[BeatSketchTrackingDataDetails]
    bpm: float


class BeatSketchTrackingDataDetails(TypedDict):
    tracking: list[np.ndarray]  # 3 elements each (x, y, z coords)
    x: int
    y: int
    beat: float


class BeatSketchPredictions(TypedDict):
    left: list[bool]
    right: list[bool]


HANDS: list[Literal["left"] | Literal["right"]] = ["left", "right"]
DATASET = tuple[np.ndarray, np.ndarray]
MODELS = Literal["testing"] | Literal["mlp"]
