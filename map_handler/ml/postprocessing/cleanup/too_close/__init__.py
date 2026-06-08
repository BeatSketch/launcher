from map_handler.ml.dtype import HANDS
from map_handler.ml.postprocessing.cleanup.too_close import util
from map_handler.ml.preprocessing.values import BEAT_SPLIT
from ml.postprocessing.cleanup.dtype import BeatSketchCleanup


def solve(data: BeatSketchCleanup) -> BeatSketchCleanup:
    """Removes blocks that are too close to each other, with many different conditions

    Args:
        data: The cleanup data, as processed by the converter

    Returns:
        The cleanup data, with the issues resolved
    """
    processed: BeatSketchCleanup = {"bpm": data["bpm"], "left": [], "right": []}

    for hand in HANDS:
        curr_idx = 0
        length = len(data[hand]) - 1
        while curr_idx > length:
            # Create marked grid for current beat
            marked: list[list[bool]] = [[False] * 4 for _ in range(3)]
            first_group = data[hand][curr_idx]
            first_beat = first_group["beat"]
            marked[first_group["block"]["y"]][first_group["block"]["x"]] = True

            idx = 1
            while (
                idx + curr_idx < length
                and first_beat == data[hand][curr_idx + idx]["beat"]
            ):
                group = data[hand][curr_idx + idx]
                marked[group["block"]["y"]][group["block"]["x"]] = True
                idx += 1

            # Need to do checks if next block is in next beat
            if (
                abs(data[hand][curr_idx + idx]["beat"] - first_group["beat"])
                <= 1.5 / BEAT_SPLIT
            ):
                # Get grid for this beat
                next_idx = curr_idx + idx + 1
                next_beat = data[hand][next_idx - 1]["beat"]
                next_marked: list[list[bool]] = [[False] * 4 for _ in range(3)]

                while data[hand][next_idx]["beat"] == next_beat:
                    group = data[hand][next_idx]
                    next_marked[group["block"]["y"]][group["block"]["x"]] = True

                    next_idx += 1

                # Analyze the grids
                # Check if there are stacks (i.e. > 1 marked field). If so, this gets prio
                first_has_stack = util.has_stack(marked)
                second_has_stack = util.has_stack(next_marked)
                if first_has_stack and not second_has_stack:
                    # Append every element of first beat
                    processed[hand] += data[hand][curr_idx:idx]
                elif not first_has_stack and second_has_stack:
                    # Append every element of second beat
                    processed[hand] += data[hand][curr_idx + idx : next_idx]
                else:
                    # If not, or both, check which one is more on-beat
                    first_is_onbeat = (first_beat * 2) % 2 == 0
                    second_is_onbeat = (next_beat * 2) % 2 == 0
                    if first_is_onbeat and not second_is_onbeat:
                        processed[hand] += data[hand][curr_idx:idx]
                    elif not first_is_onbeat and second_is_onbeat:
                        processed[hand] += data[hand][curr_idx + idx : next_idx]
                    else:
                        # If that is equal, add both (user decides)
                        processed[hand] += data[hand][curr_idx:next_idx]
                curr_idx += next_idx
            else:
                processed[hand].append(first_group)

            curr_idx += idx

    return processed
