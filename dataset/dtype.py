from typing import TypedDict


class BeatSketchTrackingData(TypedDict):
    left: list[float]
    right: list[float]
    time: float


class BeatSketchTrainingData(TypedDict):
    left: list[float]
    right: list[float]
    time: float


class BeatSketchBlocks(TypedDict):
    orientation: int
    x: int
    y: int
    time: float
    is_right_hand: bool
    good_cut: bool
