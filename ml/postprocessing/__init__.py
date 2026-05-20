from ml.dtype import HANDS, BeatSketchTrackingData, BeatSketchPredictions
from ml.postprocessing import blocks
from util.ipc.decode import BeatSketchBlock


def postprocess(data: BeatSketchTrackingData, predictions: BeatSketchPredictions):
    processed: list[BeatSketchBlock] = []
    for hand in HANDS:
        processed += blocks.generate(data[hand], predictions[hand], hand)

    return processed
