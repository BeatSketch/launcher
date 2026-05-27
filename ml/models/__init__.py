from ml.dtype import DATASET, HANDS, BeatSketchPredictions, MODELS
from ml.models.interface import MlModelInterface
from ml.models.onnx import ONNXModel
from ml.models.testing import TestingModel

# TODO: Add the correct models
models: dict[MODELS, tuple[type[MlModelInterface], str]] = {
    "testing": (TestingModel, "TEST"),
    "mlp": (ONNXModel, "mlp.onnx"),
}


def create_predictions(model: MODELS, data: DATASET, models_folder: str):
    """Run the data through the specified model

    Args:
        model: The model to use for the processing
        data: The data to process

    Returns:
        A list with the indices corresponding to the ones in the data, containing a bool
        indicating if the corresponding field should be filled
    """
    predictions: BeatSketchPredictions = {"left": [], "right": []}
    loaded_model = load_model(model, models_folder)
    for idx, hand in enumerate(HANDS):
        if data[idx].shape[0] != 0:
            predictions[hand] = loaded_model.predict(data[idx])

    return predictions


def load_model(model: MODELS, models_folder: str):
    if not models_folder.endswith("/"):
        models_folder += "/"

    return models[model][0](models_folder + models[model][1])
