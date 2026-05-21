from ml.dtype import DATASET, HANDS, BeatSketchPredictions, MODELS
from ml.models.interface import MlModelInterface
from ml.models.testing import TestingModel

# TODO: Add the correct models
models: dict[MODELS, MlModelInterface] = {"testing": TestingModel("")}


def create_predictions(model: MODELS, data: DATASET):
    """Run the data through the specified model

    Args:
        model: The model to use for the processing
        data: The data to process

    Returns:
        A list with the indices corresponding to the ones in the data, containing a bool
        indicating if the corresponding field should be filled
    """
    predictions: BeatSketchPredictions = {"left": [], "right": []}
    for idx, hand in enumerate(HANDS):
        predictions[hand] = models[model].predict(data[idx])

    return predictions
