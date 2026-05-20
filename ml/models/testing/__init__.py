from ml.models.interface import MlModelInterface
import random
import numpy as np


class TestingModel(MlModelInterface):
    def __init__(self, model_path: str) -> None:
        print("Loading test model, path would be", model_path)
        pass

    def predict(self, data: np.ndarray) -> list[bool]:
        # randomly return True or False for each data point
        pred = []
        for _ in range(len(data)):
            pred.append(random.randint(0, 3) == 2)

        return pred
