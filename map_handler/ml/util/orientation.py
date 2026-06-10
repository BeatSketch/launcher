from typing import Literal
from map_handler.ml.dtype import BeatSketchTrackingDataDetails
from map_handler.ml.preprocessing.values import (
    GRID_FIELD_HEIGHT,
    GRID_FIELD_WIDTH,
    GRID_X_MIN_VAL,
    GRID_Y_MIN_VAL,
)
from map_handler.map.dtype.beatmap import CutDirection
import numpy as np


base_vec = np.array([0, 1, 0])
translation = [
    CutDirection.UP,
    CutDirection.UP_LEFT,
    CutDirection.LEFT,
    CutDirection.DOWN_LEFT,
    CutDirection.DOWN,
    CutDirection.DOWN_RIGHT,
    CutDirection.RIGHT,
    CutDirection.UP_RIGHT,
]


def determine_cut_direction(
    data: BeatSketchTrackingDataDetails,
    strat: (
        Literal["average"] | Literal["startend"] | Literal["block-scoped"]
    ) = "block-scoped",
) -> CutDirection:
    """Determine in which direction the cut happened.
    Combines the other two functions provided by this script

    Args:
        data: The data to process
        strat:
            The way in which the direction is determined. There are two options:
                - average (taking the average direction vector)
                - startend (difference between start and end points)

    Returns:
        The CutDirection of the block
    """
    count = len(data["tracking"])
    tracking = np.array(data["tracking"])[:, :3]
    orientation = CutDirection.UP
    vec = np.array([])
    if strat == "startend":
        vec = tracking[-1] - tracking[0]
        orientation = get_orientation(compute_angle(vec))
    elif strat == "average":
        # Numpy magic
        vec: np.ndarray = (tracking[1:] - tracking[:-1]).sum(0) / (count - 1)
        orientation = get_orientation(compute_angle(vec))
    elif strat == "block-scoped":
        # Only use the tracking data that concerns this block directly
        inside: list[int] = []
        col = data["x"]
        line = data["y"]
        for idx, pos in enumerate(tracking):
            if (
                pos[0] <= GRID_X_MIN_VAL + (col + 1) * GRID_FIELD_WIDTH
                and pos[0] > GRID_X_MIN_VAL + col * GRID_FIELD_WIDTH
                and (
                    pos[1] <= GRID_Y_MIN_VAL + (line + 1) * GRID_FIELD_HEIGHT
                    and pos[1] > GRID_Y_MIN_VAL + line * GRID_FIELD_HEIGHT
                )
            ):
                inside.append(idx)

        if len(inside) > 1:
            orientation = get_orientation(
                compute_angle(tracking[inside[-1]] - tracking[inside[0]])
            )
        elif len(inside) == 1:
            if inside[0] == 0:
                orientation = get_orientation(compute_angle(tracking[1] - tracking[0]))
            else:
                orientation = get_orientation(
                    compute_angle(tracking[inside[0]] - tracking[inside[0] - 1])
                )
        else:
            # Fall back to startend method
            vec = tracking[-1] - tracking[0]
            orientation = get_orientation(compute_angle(vec))

    return orientation


def get_simple_direction(angle: float) -> int:
    return int(((angle + 22.5) % 360) // 45)


def compute_angle(vec: np.ndarray) -> float:
    """Compute the cut angle from a direction vector

    Args:
        vec: The direction vector to compute from

    Returns:
        The cut angle
    """
    # Do cheapo projection (just setting the z axis to 0) to compute the cut angle
    if vec.size == 2:
        vec = np.append(vec, 0)
    else:
        vec[2] = 0

    # Prevent zero division error
    norm = np.linalg.norm(vec)
    if norm == 0:
        return 0

    # Compute the angle
    angle = np.arccos(vec.dot(base_vec) / norm) / np.pi * 180
    cross = np.linalg.cross(base_vec, vec)
    left_side = cross[2] < 0
    return 360 - angle if left_side else angle


def get_orientation(angle: float) -> CutDirection:
    """Get the CutDirection from an angle

    Args:
        angle: The cut angle

    Returns:
        The cut direction
    """
    loc = int(((angle + 22.5) % 360) // 45)

    return translation[loc]
