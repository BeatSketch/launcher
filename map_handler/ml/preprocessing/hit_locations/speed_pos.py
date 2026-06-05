import numpy as np


def from_tracking_array(tracking: np.ndarray):
    return (np.linalg.vector_norm(tracking[1:] - tracking[:-1])).sum()
