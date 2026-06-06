from typing import Literal
from map_handler.ml.preprocessing.hit_locations import speed_pos
from map_handler.ml.preprocessing.values import (
    GRID_FIELD_HEIGHT,
    GRID_FIELD_WIDTH,
    GRID_X_MIN_VAL,
    GRID_Y_MIN_VAL,
    SPD_THRESHOLD,
    TRACKING_PER_UNIT,
)
import numpy as np


def hit_locations(
    tracking: list[np.ndarray[tuple[Literal[7]], np.dtype[np.float64]]],
    # prev: np.ndarray,
) -> list[tuple[int, int]]:
    locations: list[tuple[int, int]] = []
    """Determine possible locations where a block could be placed.
    Already includes filtering such that impossible hits can't even be generated

    Args:
        tracking: The tracking data to process

    Returns:
        A list of coordinates on the grid that were touched by the tip
    """
    # Check if total speed is lower than threshold
    # TODO: possibly use the total distance instead?
    data = np.array(tracking)
    if speed_pos.overall(data) < SPD_THRESHOLD * (TRACKING_PER_UNIT - 1):
        return []

    # Check if speed is too slow for block slice to be recognized
    vecs = speed_pos.direction_vectors(data)
    spd_ok = speed_pos.speed_from_dir_vecs(vecs) > SPD_THRESHOLD
    x = np.astype((data[:, 0] / GRID_FIELD_WIDTH).round() - GRID_X_MIN_VAL, np.int32)[
        spd_ok
    ]
    y = np.astype((data[:, 1] / GRID_FIELD_HEIGHT).round() - GRID_Y_MIN_VAL, np.int32)[
        spd_ok
    ]
    # Clamp it to 0-3 and 0-2 respectively
    x_filtered = x[x >= 0 and x < 4]
    y_filtered = y[y >= 0 and y < 3]

    # Check that there are no neighbouring blocks parallel to cut direction
    # These would not be valid anyway, so we don't send them to the classifier
    # and would need to be cleaned up afterwards anyway
    for idx, coord in enumerate(x_filtered):
        locations.append((coord, y_filtered[idx]))

    # TODO:
    # Iterate over tracking tracking vectors, compute the normals, determine the neighbouring blocks
    # then check if locations include the location, if so, apply tie-breaker (distance to the point)
    for vec in vecs:
        pass

    return locations
