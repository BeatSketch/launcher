from ml.dtype import BeatSketchPredictions, BeatSketchTrackingData
from util.dtype import BeatSketchBlock


def solve_block_collisions(
    tracking: BeatSketchTrackingData,
    pred: BeatSketchPredictions,
    blocks: list[BeatSketchBlock],
) -> list[BeatSketchBlock]:
    """Removes the most sensible blocks from collisions,
    i.e. places where two blocks occupy the same spot

    Args:
        tracking: The tracking data in the intermediary format
        pred: The predictions for this data
        blocks: The blocks that were generated from the data

    Returns:
        The blocks, with the issues resolved
    """
    processed: list[BeatSketchBlock] = []

    return processed
