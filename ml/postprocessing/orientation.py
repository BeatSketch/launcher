from typing import Literal
from ml.dtype import BeatSketchTrackingDataDetails
import numpy as np

from util.map.dtype.beatmap import CutDirection

# TODO: Check what base vector produces correct results (likely will be e_y)
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
    strat: Literal["average"] | Literal["startend"] = "startend",
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
    if strat == "startend":
        return get_orientation(compute_angle(tracking[-1] - tracking[0]))
    elif strat == "average":
        # Numpy magic
        avgs: np.ndarray = (tracking[1:] - tracking[:-1]).sum(0) / (count - 1)
        return get_orientation(compute_angle(avgs))


def compute_angle(vec: np.ndarray) -> float:
    """Compute the cut angle from a direction vector

    Args:
        vec: The direction vector to compute from

    Returns:
        The cut angle
    """
    # Do cheapo projection (just setting the z axis to 0) to compute the cut angle
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
