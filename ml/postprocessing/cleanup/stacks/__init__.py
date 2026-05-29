from ml.dtype import BeatSketchPredictions, BeatSketchTrackingData
from util.dtype import BeatSketchBlock


def fix_stacks(
    tracking: BeatSketchTrackingData,
    pred: BeatSketchPredictions,
    blocks: list[BeatSketchBlock],
) -> list[BeatSketchBlock]:
    """Fixes up block stacks by moving them into the the same beat and removing any superfluous blocks.
    Also removes any other block for the same hand in this frame, previous and subsequent ones (or two)
    to improve readbility, as well as blocks from the other hand that are too close to be reasonably
    playable

    Args:
        tracking: The tracking data in the intermediary format
        pred: The predictions for this data
        blocks: The blocks that were generated from the data

    Returns:
        The blocks, with the issues resolved
    """
    processed: list[BeatSketchBlock] = []

    return processed
