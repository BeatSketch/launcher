from map_handler.ml.dtype import HANDS
from map_handler.ml.postprocessing.cleanup.dtype import BeatSketchCleanup


def solve_hand_mixups(data: BeatSketchCleanup) -> BeatSketchCleanup:
    """May recolour blocks that are deemed to be assigned to the wrong hand.
    This is caused by the precedences of the colours. Parts of this cannot be disabled

    Args:
        data: The cleanup data, as processed by the converter

    Returns:
        The cleanup data, with the issues resolved
    """
    processed: BeatSketchCleanup = {"bpm": data["bpm"], "left": [], "right": []}

    for hand in HANDS:
        for group in data[hand]:
            pass

    return processed
