from ml.dtype import HANDS
from ml.postprocessing.orientation import compute_angle
from ml.preprocessing.values import (
    BEAT_SPLIT,
    GRID_FIELD_HEIGHT,
    GRID_FIELD_WIDTH,
    GRID_X_MIN_VAL,
    GRID_Y_MIN_VAL,
)
from ml.postprocessing.cleanup.dtype import BeatSketchCleanup, BeatSketchCleanupGroup
from ml.postprocessing.cleanup.impossible_hits.util import process
import numpy as np

angles: list[int] = [0, 180, 90, 270, 45, 315, 135, 225]


def solve(data: BeatSketchCleanup) -> BeatSketchCleanup:
    """Removes the most sensible blocks from impossible patterns
    such as having two blocks in the same direction next to each other

    Args:
        data: The cleanup data, as processed by the converter

    Returns:
        The cleanup data, with the issues resolved
    """
    """Removes the most sensible blocks from a pattern of blocks that share similar directions
    and are placed next to each other, making hitting them impossible

    Args:
        data: The cleanup data, as processed by the converter

    Returns:
        The cleanup data, with the issues resolved
    """
    processed: BeatSketchCleanup = {"bpm": data["bpm"], "left": [], "right": []}

    for hand in HANDS:
        curr_idx = 0
        group = data[hand]
        length = len(group)
        while curr_idx < length:
            # Construct graph for hit-ability check
            idx = 0
            curr_beat = group[curr_idx]["beat"]

            # Map into grid
            grid = [[-1] * 4] * 3
            while (
                curr_idx + idx < length and group[curr_idx + idx]["beat"] == curr_beat
            ):
                block = group[curr_idx + idx]["block"]
                grid[block["y"]][block["x"]] = curr_idx + idx

                idx += 1

            min_dist = 1000000
            min_idx = 0
            first_cut_dir = compute_angle(
                group[curr_idx]["tracking"][1][:3] - group[curr_idx]["tracking"][0][:3]
            )
            for i in range(idx):
                curr = group[curr_idx + i]
                angle = angles[curr["block"]["orientation"].value]

                if _center_dist(curr) < min_dist and abs(angle - first_cut_dir) < 50:
                    min_idx = i

            block = group[curr_idx + min_idx]["block"]
            okay = process(block["x"], block["y"], grid, group)
            for idx in okay:
                processed[hand].append(group[idx])

            # Look at future blocks to see if there is a block that is too close
            while (
                curr_idx + idx < length
                and group[curr_idx + idx]["beat"] <= curr_beat + 1.1 / BEAT_SPLIT
            ):
                idx += 1

            # Above removal is implicit (block is skipped)
            curr_idx += idx

    return processed


def _center_dist(data: BeatSketchCleanupGroup):
    """Compute the minimum distance to centre for the tracking data

    Args:
        data: The cleanup group to compute for

    Returns:
        The distance from centre
    """
    tracking = np.array(data["tracking"])
    x = data["block"]["x"]
    y = data["block"]["y"]

    squares_x = (
        tracking[:, 0]
        - (GRID_X_MIN_VAL + x * GRID_FIELD_WIDTH + 0.5 * GRID_FIELD_WIDTH)
    ) ** 2
    squares_y = (
        tracking[:, 1]
        - (GRID_Y_MIN_VAL + y * GRID_FIELD_HEIGHT + 0.5 * GRID_FIELD_HEIGHT)
    ) ** 2
    return np.sqrt(squares_x.min() + squares_y.min())
