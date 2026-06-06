from typing import Literal

import numpy as np
from map_handler.ml.preprocessing.values import (
    GRID_FIELD_HEIGHT,
    GRID_FIELD_WIDTH,
    GRID_X_MIN_VAL,
    GRID_Y_MIN_VAL,
)


def compute(tracking: np.ndarray, x: int, y: int, mode: Literal["x", "y", "both"] = "both"):
    """Compute the minimum distance to centre for the tracking data

    Args:
        tracking: Numpy array containing the tracking data
        x: The x coordinate of the block
        y: The y coordinate of the block

    Returns:
        The distance from centre
    """
    squares_x = (
        tracking[:, 0]
        - (GRID_X_MIN_VAL + x * GRID_FIELD_WIDTH + 0.5 * GRID_FIELD_WIDTH)
    )
    squares_y = (
        tracking[:, 1]
        - (GRID_Y_MIN_VAL + y * GRID_FIELD_HEIGHT + 0.5 * GRID_FIELD_HEIGHT)
    )
    if mode == "both":
        return np.sqrt(squares_x.min() ** 2 + squares_y.min() ** 2)
    elif mode == "x":
        return squares_x.min()
    elif mode == "y":
        return squares_y.min()
