from typing import Literal

from ml.dtype import HANDS, BeatSketchPredictions, BeatSketchTrackingData
from ml.models.interface import MlModelInterface
from ml.models.testing import TestingModel

# TODO: Add the correct models
models_type = Literal["testing"] | Literal["mlp"]
models: dict[models_type, MlModelInterface] = {"testing": TestingModel("")}


def create_predictions(model: models_type, data: BeatSketchTrackingData):
    """Run the data through the specified model

    Args:
        model: The model to use for the processing
        data: The data to process

    Returns:
        A list with the indices corresponding to the ones in the data, containing a bool
        indicating if the corresponding field should be filled
    """
    predictions: BeatSketchPredictions = {"left": [], "right": []}
    for hand in HANDS:
        for tracking_data in data[hand]:
            predictions[hand].append(models[model].predict(tracking_data))

    return predictions
