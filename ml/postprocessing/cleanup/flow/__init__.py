from ml.dtype import HANDS
from ml.postprocessing.cleanup.dtype import BeatSketchCleanup


def solve_flow_issues(data: BeatSketchCleanup) -> BeatSketchCleanup:
    """May change the cut direction of a block, or mark it as any direction,
    if a specific pattern is recognized

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
