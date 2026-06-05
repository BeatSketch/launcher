from typing import Literal
from map_handler.ml.preprocessing.hit_locations import speed_pos
from map_handler.ml.preprocessing.values import (
    GRID_FIELD_HEIGHT,
    GRID_FIELD_WIDTH,
    GRID_X_MIN_VAL,
    GRID_Y_MIN_VAL,
    THRESHOLD,
)
import numpy as np


def hit_locations(
    tracking: list[np.ndarray[tuple[Literal[7]], np.dtype[np.float64]]],
    # prev: np.ndarray,
) -> list[tuple[int, int]]:
    locations: list[tuple[int, int]] = []
    """Determine possible locations where a block could be placed

    Args:
        tracking: The tracking data to process

    Returns:
        A list of coordinates on the grid that were touched by the tip
    """
    # TODO: Check if total speed is lower than threshold
    # or possibly use the total distance instead
    data = np.array(tracking)
    if speed_pos.from_tracking_array(data) < THRESHOLD:
        return []

    for pos in tracking:
        hand = pos[:3]
        # TODO: Check if speed is too slow for block slice to be recognized
        for line in range(3):
            for col in range(4):
                # TODO: Improve this check to make sure the cut is not just barely hitting the location
                if (
                    hand[0] <= GRID_X_MIN_VAL + (col + 1) * GRID_FIELD_WIDTH
                    and hand[0] > GRID_X_MIN_VAL + col * GRID_FIELD_WIDTH
                    and (
                        (
                            hand[1] <= GRID_Y_MIN_VAL + (line + 1) * GRID_FIELD_HEIGHT
                            and hand[1] > GRID_Y_MIN_VAL + line * GRID_FIELD_HEIGHT
                        )
                    )
                ):
                    try:
                        locations.index((col, line))
                    except Exception:
                        locations.append((col, line))

    # TODO: Check that there are no neighbouring blocks parallel to cut direction
    # These would not be valid anyway, so we don't send them to the classifier
    # and would need to be cleaned up afterwards anyway

    return locations
