import numpy as np

from map_handler.ml.preprocessing.values import BEAT_SPLIT

base_vecs = np.array([[0.0, 0.0, 1.0] * 10])


def overall(tracking: np.ndarray):
    time_delta = (
        tracking[-1][6] - tracking[0][6]
        if tracking.shape[0] > 1
        else 1 / 120 * BEAT_SPLIT
    )
    return between_points(tracking).sum() / time_delta


def time_deltas(tracking: np.ndarray):
    return tracking[:-1, 6] - tracking[1:, 6]


def speed_from_dir_vecs(vectors: np.ndarray, time_delta: np.ndarray):
    # TODO: Extrapolate first point
    spd = np.linalg.vector_norm(vectors) / time_delta
    return np.concatenate(([0], spd))


def between_points(tracking: np.ndarray):
    return np.linalg.vector_norm(tracking[1:, :2] - tracking[:-1, :2])


def direction_vectors(tracking: np.ndarray):
    return tracking[1:, :2] - tracking[:-1, :2]


def compute_normals(vectors: np.ndarray):
    # Cross product on 0, 0, 1 vec and x, y, 0 vec (from the vectors)
    vectors[:, 2] = 0.0
    return np.linalg.cross(vectors, base_vecs[: vectors.shape[0]])[:, :2]
