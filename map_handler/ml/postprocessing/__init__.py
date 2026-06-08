from map_handler.ml.dtype import HANDS, BeatSketchTrackingData, BeatSketchPredictions
from map_handler.ml.postprocessing import blocks, cleanup
from map_handler.dtype import BeatSketchBlock
from map_handler.ml.config import enable_heuristics


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

    if enable_heuristics:
        return cleanup.clean_up_classifier_output(data, predictions, processed, dev_mode)
    else:
        return processed
