import numpy as np

from map_handler.ml.preprocessing.values import BEAT_SPLIT

base_vec = np.array([0, 0, 1])


def overall(tracking: np.ndarray):
    time_delta = (
        tracking[-1][6] - tracking[0][6]
        if tracking.shape[0] > 1
        else 1 / 120 * BEAT_SPLIT
    )
    return between_points(tracking).sum() / time_delta


def speed_from_dir_vecs(vectors: np.ndarray):
    return np.linalg.vector_norm(vectors)


def between_points(tracking: np.ndarray):
    return np.linalg.vector_norm(tracking[1:, :3] - tracking[:-1, :3])


def direction_vectors(tracking: np.ndarray):
    return tracking[1:, :3] - tracking[:-1, :3]


def compute_normals(vectors: np.ndarray):
    # Cross product on 0, 0, 1 vec and x, y, 0 vec (from the vectors)
    pass
