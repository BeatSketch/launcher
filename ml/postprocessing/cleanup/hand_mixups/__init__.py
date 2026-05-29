from ml.dtype import BeatSketchPredictions, BeatSketchTrackingData
from util.dtype import BeatSketchBlock


def solve_hand_mixups(
    tracking: BeatSketchTrackingData,
    pred: BeatSketchPredictions,
    blocks: list[BeatSketchBlock],
) -> list[BeatSketchBlock]:
    """May recolour blocks that are deemed to be assigned to the wrong hand.
    This is caused by the precedences of the colours. Parts of this cannot be disabled

    Args:
        tracking: The tracking data in the intermediary format
        pred: The predictions for this data
        blocks: The blocks that were generated from the data

    Returns:
        The blocks, with the issues resolved
    """
    processed: list[BeatSketchBlock] = []

    return processed
