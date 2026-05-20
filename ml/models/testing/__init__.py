from ml.dtype import BeatSketchTrackingDataDetails
from ml.models.interface import MlModelInterface
import random


class TestingModel(MlModelInterface):
    def __init__(self, model_path: str) -> None:
        pass

    def predict(self, data: BeatSketchTrackingDataDetails) -> bool:
        # randomly return True or False
        return random.randint(0, 3) == 2
