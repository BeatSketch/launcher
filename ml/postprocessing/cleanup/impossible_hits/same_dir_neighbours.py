from ml.dtype import BeatSketchPredictions, BeatSketchTrackingData
from util.dtype import BeatSketchBlock


def solve_same_dir_neighbours(
    tracking: BeatSketchTrackingData,
    pred: BeatSketchPredictions,
    blocks: list[BeatSketchBlock],
) -> list[BeatSketchBlock]:
    """Removes the most sensible blocks from a pattern of blocks that share similar directions
    and are placed next to each other, making hitting them impossible

    Args:
        tracking: The tracking data in the intermediary format
        pred: The predictions for this data
        blocks: The blocks that were generated from the data

    Returns:
        The blocks, with the issues resolved
    """
    processed: list[BeatSketchBlock] = []

    return processed
