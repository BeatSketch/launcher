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
    if speed_pos.overall(data) < SPD_THRESHOLD * TRACKING_PER_UNIT * 0.5:
        return []

    # Check if speed is too slow for block slice to be recognized
    vecs = speed_pos.direction_vectors(data)
    speeds = speed_pos.speed_from_dir_vecs(vecs, speed_pos.time_deltas(data))
    spd_ok = speeds > SPD_THRESHOLD
    x = np.astype((data[:, 0] / GRID_FIELD_WIDTH).round() - GRID_X_MIN_VAL, np.int32)[
        spd_ok
    ]
    y = np.astype((data[:, 1] / GRID_FIELD_HEIGHT).round() - GRID_Y_MIN_VAL, np.int32)[
        spd_ok
    ]

    # Clamp it to 0-3 and 0-2 respectively
    if x.size == 0:
        return []
    clamp = (x >= 0) & (x < 4) & (y >= 0) & (y < 3)
    x_filtered = x[clamp]
    y_filtered = y[clamp]
    data_filtered = (data[spd_ok])[clamp]

    # Check that there are no neighbouring blocks parallel to cut direction
    # These would not be valid anyway, so we don't send them to the classifier
    # and would need to be cleaned up afterwards anyway
    # FIXME: Looks like something here is messing up
    marked: list[list[bool]] = [[False] * 4] * 3
    for idx, x_coord in enumerate(x_filtered):
        if idx == 0:
            o = orientation.get_simple_direction(orientation.compute_angle(vecs[0]))
        else:
            o = orientation.get_simple_direction(
                orientation.compute_angle(vecs[idx - 1])
            )
        tiebreaker.execute(data_filtered[idx], marked, x_coord, y_filtered[idx], o)

    # Convert marks into list
    for y_coord, layers in enumerate(marked):
        for x_coord, is_set in enumerate(layers):
            if is_set:
                locations.append((y_coord, x_coord))

    # TODO: Remove duplicates

    return locations
