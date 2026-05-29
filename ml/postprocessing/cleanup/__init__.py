from ml.dtype import BeatSketchPredictions, BeatSketchTrackingData
from util.dtype import BeatSketchBlock


def clean_up_classifier_output(
    tracking: BeatSketchTrackingData,
    pred: BeatSketchPredictions,
    blocks: list[BeatSketchBlock],
) -> list[BeatSketchBlock]:
    """Cleans up the map using heuristics, removing impossible to slice structures that the
    classifier may generate. Features can be enabled, disabled and configured in the config file

    Args:
        tracking: The tracking data in the intermediary format
        pred: The predictions for this data
        blocks: The blocks that were generated from the data

    Returns:
        The blocks, with the issues resolved
    """
    processed: list[BeatSketchBlock] = []

    # Order matters:
    # 1. stacks
    # 2. collisions
    # 2. impossible hits
    # 3. Flow
    # 4. hand mixups
    # The idea is to chain these into one another

    return processed
