from ml.dtype import DATASET, BeatSketchTrackingData
from ml.preprocessing.dataset import generate_model_readable_data
from ml.preprocessing.prepare import prepare as _prepare
from util.dtype import BeatSketchVRData


def preprocess(
    data: list[BeatSketchVRData], bpm: int, njs: float
) -> tuple[DATASET, BeatSketchTrackingData]:
    """Preprocess the data into the dataset, as can be used by the models
    and the tracking data, as it is used by the postprocessor

    Args:
        data: The VR data to be transformed
        bpm: The BPM of the song
        njs: The Note Jump Speed of the song

    Returns:
        A tuple containing first the model-compatible data,
        then the postprocessor-compatible data
    """
    prepared = _prepare(data, bpm, njs)
    return generate_model_readable_data(prepared), prepared
