from ml.models import models_type, create_predictions
from ml.postprocessing import postprocess
from ml.preprocessing import preprocess
from util.ipc.decode import BeatSketchBlock, BeatSketchVRData


def process(
    data: list[BeatSketchVRData],
    bpm: int,
    njs: float,
    model: models_type,
) -> list[BeatSketchBlock]:
    preprocessed, orig = preprocess(data, bpm, njs)
    pred = create_predictions(model, preprocessed)
    return postprocess(orig, pred)
