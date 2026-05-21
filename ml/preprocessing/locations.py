from ml.preprocessing.values import GRID_FIELD_HEIGHT, GRID_FIELD_WIDTH, GRID_X_MIN_VAL, GRID_Y_MIN_VAL, THRESHOLD
import numpy as np


def hit_locations(
    tracking: list[np.ndarray],
) -> list[tuple[int, int]]:
    locations: list[tuple[int, int]] = []
    """Determine possible locations where a block could be placed

    Args:
        tracking: The tracking data to process

    Returns:
        A list of coordinates on the grid that were touched by the tip
    """
    for pos in tracking:
        hand = pos[:3]
        dir = pos[3:]
        for line in range(3):
            for col in range(4):
                if (
                    hand[0] < GRID_X_MIN_VAL + (col + 1) * GRID_FIELD_WIDTH
                    and hand[0] > GRID_X_MIN_VAL + col * GRID_FIELD_WIDTH
                    and (
                        (
                            hand[1] < GRID_Y_MIN_VAL + (line + 1) * GRID_FIELD_HEIGHT
                            and hand[1] > GRID_Y_MIN_VAL + line * GRID_FIELD_HEIGHT
                        )
                        or (
                            hand[1] - THRESHOLD * dir[1]
                            < GRID_Y_MIN_VAL + (line + 1) * GRID_FIELD_HEIGHT
                            and hand[1] - THRESHOLD * dir[1]
                            > GRID_Y_MIN_VAL + line * GRID_FIELD_HEIGHT
                        )
                    )
                ):
                    try:
                        locations.index((line, col))
                    except Exception:
                        locations.append((line, col))

    return locations
