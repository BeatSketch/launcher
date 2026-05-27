from ml.dtype import HANDS, BeatSketchTrackingData, BeatSketchPredictions
from ml.postprocessing import blocks
from util.dtype import BeatSketchBlock


def postprocess(
    data: BeatSketchTrackingData, predictions: BeatSketchPredictions
) -> list[BeatSketchBlock]:
    """Postprocess the data and generate blocks from it

    Args:
        data: The tracking data
        predictions: The predictions from the model

    Returns:
        The generated blocks
    """
    processed: list[BeatSketchBlock] = []
    for hand in HANDS:
        processed += blocks.generate(data[hand], predictions[hand], hand)

    return processed
