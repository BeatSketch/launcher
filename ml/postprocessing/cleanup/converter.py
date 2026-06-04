from ml.dtype import HANDS, BeatSketchPredictions, BeatSketchTrackingData
from ml.postprocessing.cleanup.dtype import BeatSketchCleanup
from util.dtype import BeatSketchBlock


def to_cleanup_format(
    tracking: BeatSketchTrackingData,
    pred: BeatSketchPredictions,
    blocks: list[BeatSketchBlock],
) -> BeatSketchCleanup:
    """Convert the three passed in formats into a single
    simple format that can easily be used by the cleanup scripts

    Args:
        tracking: The tracking data
        pred: The preditions from the models
        blocks: The blocks that were generated from the tracking data and predictions

    Returns:
        The passed in data in the cleanup format.
        Blocks can be extracted from the format again using to_blocks function
    """
    data: BeatSketchCleanup = {"left": [], "right": [], "bpm": tracking["bpm"]}
    block_idx = 0
    for hand in HANDS:
        predictions = pred[hand]
        for idx, tracked in enumerate(tracking[hand]):
            if predictions[idx]:
                # Form the groups
                data[hand].append(
                    {
                        "block": blocks[block_idx],
                        "tracking": tracked["tracking"],
                        "beat": tracked["beat"],
                    }
                )

                block_idx += 1

    return data


def to_blocks(data: BeatSketchCleanup) -> list[BeatSketchBlock]:
    """Takes the cleanup data format and returns the contained blocks

    Args:
        data: Cleanup data format

    Returns:
        The extracted blocks
    """
    blocks: list[BeatSketchBlock] = []
    for group in data["left"]:
        blocks.append(group["block"])

    for group in data["right"]:
        blocks.append(group["block"])

    return blocks
