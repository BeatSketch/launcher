from typing import Literal

import numpy as np

from map_handler.ml.util import center_distance


def execute(point: np.ndarray, marked: list[list[bool]], x: int, y: int, o: int):
    def _resolve(x_comp: int, y_comp: int, coord: Literal["x", "y"]):
        if center_distance.compute(point, x, y, coord) < center_distance.compute(
            point, x_comp, y_comp, coord
        ):
            marked[y_comp][x_comp] = False
            marked[y][x] = True
        else:
            marked[y][x] = False
            marked[y_comp][x_comp] = True

    # Treat horizontals and verticals (up to 3 locations)
    if o == 0 or o == 4:
        # Horizontals
        if x < 3 and marked[y][x + 1]:
            _resolve(x + 1, y, "x")
        elif x > 0 and marked[y][x - 1]:
            _resolve(x - 1, y, "x")
        else:
            marked[y][x] = True
    elif o == 2 or o == 6:
        # Verticals
        if y < 2 and marked[y + 1][x]:
            _resolve(x, y + 1, "y")
        elif y > 0 and marked[y - 1][x]:
            _resolve(x, y - 1, "y")
        else:
            marked[y][x] = True
    # TODO: What to do with diagonal cuts? (They can be tricky)
