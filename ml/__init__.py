from ml.models import (
    MODELS as _MODELS,
    create_predictions as _create_predictions,
)
from ml.postprocessing import postprocess as _postprocess
from ml.preprocessing import preprocess as _preprocess
from util.ipc.decode import BeatSketchBlock, BeatSketchVRData


def process(
    data: list[BeatSketchVRData],
    bpm: int,
    njs: float,
    model: _MODELS,
) -> list[BeatSketchBlock]:
    """Run the tracking data through the model chain.
    All pre and postprocessing happens automatically. Pick a model from the available models

    Args:
        data: The tracking data, as received from the VR application
        bpm: The BPM of the song
        njs: The Note Jump Speed of the song
        model: The MachineLearning model to use

    Returns:
        A list of blocks that the model "thinks" best match the movement
    """
    preprocessed, orig = _preprocess(data, bpm, njs)
    pred = _create_predictions(model, preprocessed)
    post = _postprocess(orig, pred)
    return post
