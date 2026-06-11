# Interface definition of a model handler
from abc import ABC, abstractmethod
from numpy import ndarray


class MlModelInterface(ABC):
    @abstractmethod
    def __init__(self, model_path: str, input_name: str = "X") -> None:
        """Loading of the model and any processing that can take place before
        predicting

        Args:
            model_path: File path to the model
        """
        super().__init__()

    @abstractmethod
    def predict(self, data: ndarray) -> list[bool]:
        """Apply the model to the data

        Args:
            data: The data to run the prediction on

        Returns:
            A list of predictions, which are booleans indicating if in the specified point,
            there is a block or not.
            The indices correspond to the ones in the input data.
        """
        pass
