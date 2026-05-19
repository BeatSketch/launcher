from typing import Literal, TypedDict
import numpy as np


class BeatSketchTrackingData(TypedDict):
    left: list[BeatSketchTrackingDataDetails]
    right: list[BeatSketchTrackingDataDetails]


class BeatSketchTrackingDataDetails(TypedDict):
    tracking: list[np.ndarray]  # 3 elements (x, y, z coords)
    hits: list[tuple[int, int]]
    beat: float


HANDS: list[Literal["left"] | Literal["right"]] = ["left", "right"]
