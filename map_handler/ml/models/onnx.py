from typing import cast
from map_handler.ml.models.interface import MlModelInterface
import onnxruntime as rt
import numpy as np


# https://scikit-learn.org/stable/model_persistence.html
# https://onnxruntime.ai/docs/api/python/tutorial.html
class ONNXModel(MlModelInterface):
    def __init__(self, model_path: str) -> None:
        with open(model_path, "rb") as f:
            model_data = f.read()
        self._session = rt.InferenceSession(
            model_data, providers=rt.get_available_providers()
        )

    def predict(self, data: np.ndarray) -> list[bool]:
        data = data.astype(np.float32)
        pred = cast(np.ndarray, self._session.run(None, {"X": data})[0])
        predictions: list[bool] = []
        for el in pred:
            if el == 1:
                predictions.append(True)
            else:
                predictions.append(False)

        return predictions
