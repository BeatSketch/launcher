from map_handler.ml.postprocessing.cleanup.dtype import (
    BeatSketchCleanup,
    BeatSketchCleanupGroup,
)
import numpy as np

from map_handler.ml.util import center_distance


def solve(data: BeatSketchCleanup) -> BeatSketchCleanup:
    """Removes the most sensible blocks from collisions,
    i.e. places where two blocks occupy the same spot

    Args:
        data: The cleanup data, as processed by the converter

    Returns:
        The cleanup data, with the issues resolved
    """
    processed: BeatSketchCleanup = {"bpm": data["bpm"], "left": [], "right": []}
    curr_idx = 0
    to_skip_idxs_right: list[int] = []

    for group in data["left"]:
        # Catch up to the current frame on the other hand
        length = len(data["right"])
        while curr_idx < length and data["right"][curr_idx]["beat"] < group["beat"]:
            curr_idx += 1

        # Check for conflicts
        conflicts: list[BeatSketchCleanupGroup] = []
        conflicts.append(group)
        conflict_idxs: list[int] = []
        while curr_idx < length and data["right"][curr_idx]["beat"] == group["beat"]:
            if (
                data["right"][curr_idx]["block"]["x"] == group["block"]["x"]
                and data["right"][curr_idx]["block"]["y"] == group["block"]["y"]
            ):
                conflicts.append(data["right"][curr_idx])
                conflict_idxs.append(curr_idx)
            curr_idx += 1

        # Resolve the conflicts if there is one
        if len(conflicts) > 1:
            ok_idx = _resolve(conflicts)
            if ok_idx == 0:
                processed["left"].append(group)
            else:
                processed["right"].append(conflicts[ok_idx])

            if ok_idx == len(conflict_idxs) - 1:
                to_skip_idxs_right += conflict_idxs[:ok_idx]
            elif ok_idx > 0:
                to_skip_idxs_right += (
                    conflict_idxs[:ok_idx] + conflict_idxs[ok_idx + 1 :]
                )
            else:
                to_skip_idxs_right += conflict_idxs
        else:
            processed["left"].append(group)

    # Add blocks for the other hand too
    curr_idx = 0
    length = len(to_skip_idxs_right)
    to_skip_idxs_right.sort()
    for idx, group in enumerate(data["right"]):
        if curr_idx < length and to_skip_idxs_right[curr_idx] == idx:
            curr_idx += 1
        else:
            processed["right"].append(group)

    return processed


def _resolve(data: list[BeatSketchCleanupGroup]):
    """Get the index in the passed in list of the element that has minimum distance

    Args:
        data: The data to process

    Returns:
        The index of the optimal element
    """
    min_dist = 10000000
    min_dist_idx = 0
    for idx, group in enumerate(data):
        dist = center_distance.compute(
            np.array(group["tracking"]), group["block"]["x"], group["block"]["y"]
        )
        if dist < min_dist:
            min_dist = dist
            min_dist_idx = idx

    return min_dist_idx
