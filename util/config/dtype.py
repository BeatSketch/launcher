from typing import Literal, TypedDict as _TypedDict


class BeatSketchConfig(_TypedDict):
    saber_angle: BeatSketchSaberAngleConfig
    default_save_path: str
    folder_loc_for_picker: str
    used_model: Literal["testing", "mlp"]
    cleanup: CleanupFunctions
    mirror: bool


class CleanupFunctions(_TypedDict):
    distance: bool
    collisions: bool


class BeatSketchSaberAngleConfig(_TypedDict):
    x: int
    y: int
    z: int
