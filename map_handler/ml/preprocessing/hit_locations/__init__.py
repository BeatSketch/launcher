from typing import Literal
from map_handler.ml.preprocessing.hit_locations import speed_pos, tiebreaker
from map_handler.ml.preprocessing.values import (
    GRID_FIELD_HEIGHT,
    GRID_FIELD_WIDTH,
    GRID_X_MIN_VAL,
    GRID_Y_MIN_VAL,
    SPD_THRESHOLD,
    TRACKING_PER_UNIT,
)
import numpy as np

from map_handler.ml.util import orientation


def hit_locations(
    tracking: list[np.ndarray[tuple[Literal[7]], np.dtype[np.float64]]],
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
    data = np.array([_extrapolate(tracking)] + tracking)
    if speed_pos.overall(data) < SPD_THRESHOLD * TRACKING_PER_UNIT * 0.5:
        return []

    # Check if speed is too slow for block slice to be recognized
    vecs = speed_pos.direction_vectors(data)
    speeds = speed_pos.speed_from_dir_vecs(vecs, speed_pos.time_deltas(data))
    spd_ok = speeds > SPD_THRESHOLD
    x = np.astype(
        ((data[1:, 0] - GRID_X_MIN_VAL) / GRID_FIELD_WIDTH).round(), np.int32
    )[spd_ok]
    y = np.astype(
        ((data[1:, 1] - GRID_Y_MIN_VAL) / GRID_FIELD_HEIGHT).round(), np.int32
    )[spd_ok]

    # Clamp it to 0-3 and 0-2 respectively
    if x.size == 0:
        return []
    clamp = (x >= 0) & (x < 4) & (y >= 0) & (y < 3)
    x_filtered = x[clamp]
    y_filtered = y[clamp]
    data_filtered = (data[1:][spd_ok])[clamp]
    vecs_filtered = (vecs[spd_ok])[clamp]

    # Check that there are no neighbouring blocks parallel to cut direction
    # These would not be valid anyway, so we don't send them to the classifier
    # and would need to be cleaned up afterwards anyway
    marked: list[list[bool]] = [[False] * 4 for _ in range(3)]
    for idx, x_coord in enumerate(x_filtered):
        if idx == 0:
            o = orientation.get_simple_direction(
                orientation.compute_angle(vecs_filtered[0])
            )
        else:
            o = orientation.get_simple_direction(
                orientation.compute_angle(vecs_filtered[idx - 1])
            )
        tiebreaker.execute(data_filtered[idx], marked, x_coord, y_filtered[idx], o)

    # Convert marks into list
    for y_coord, layers in enumerate(marked):
        for x_coord, is_set in enumerate(layers):
            if is_set:
                locations.append((y_coord, x_coord))

    return locations


def _extrapolate(tracking: list[np.ndarray]):
    vec = tracking[0] - tracking[1]
    return tracking[0] - vec
