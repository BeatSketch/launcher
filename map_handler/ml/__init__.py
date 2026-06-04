from map_handler.ml.models import (
    MODELS as _MODELS,
    create_predictions as _create_predictions,
)
from map_handler.ml.postprocessing import postprocess as _postprocess
from map_handler.ml.preprocessing import preprocess as _preprocess
from map_handler.dtype import BeatSketchBlock, BeatSketchVRData

# Optional trailing slash
MODELS_FOLDER = "./models"
MODELS_FOLDER_DEV = "../dataset/models"


def process(
    data: list[BeatSketchVRData],
    bpm: float,
    njs: float,
    model: _MODELS,
    dev_mode: bool = False
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
    preprocessed, orig = _preprocess(data, bpm, njs, dev_mode)
    pred = _create_predictions(model, preprocessed, MODELS_FOLDER_DEV if dev_mode else MODELS_FOLDER)
    return _postprocess(orig, pred, dev_mode)
