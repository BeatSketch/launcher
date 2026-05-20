# Interface definition of a model handler

from abc import ABC, abstractmethod
from ml.dtype import BeatSketchTrackingDataDetails


class MlModelInterface(ABC):
    @abstractmethod
    def __init__(self, model_path: str) -> None:
        """Loading of the model and any processing that can take place before
        predicting

        Args:
            model_path: File path to the model
        """
        super().__init__()

    @abstractmethod
    def predict(self, data: BeatSketchTrackingDataDetails) -> bool:
        """Apply the model to the data

        Args:
            data: The data to run the prediction on

        Returns:
            True if there is a block for the given data, False otherwise
        """
        pass
