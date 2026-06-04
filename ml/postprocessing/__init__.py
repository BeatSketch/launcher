from ml.dtype import HANDS, BeatSketchTrackingData, BeatSketchPredictions
from ml.postprocessing import blocks, cleanup
from util.dtype import BeatSketchBlock


def postprocess(
    data: BeatSketchTrackingData,
    predictions: BeatSketchPredictions,
    dev_mode: bool = False,
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

    return cleanup.clean_up_classifier_output(data, predictions, processed, dev_mode)
