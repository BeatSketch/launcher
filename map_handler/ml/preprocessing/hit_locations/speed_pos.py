import numpy as np

base_vecs = np.array([[0.0, 0.0, 1.0] * 10])


def overall(tracking: np.ndarray):
    return speed_from_dir_vecs(direction_vectors(tracking), time_deltas(tracking)).sum()


def time_deltas(tracking: np.ndarray):
    return tracking[:-1, 6] - tracking[1:, 6]


def speed_from_dir_vecs(vectors: np.ndarray, time_delta: np.ndarray):
    # TODO: Extrapolate first point
    spd = np.abs(np.linalg.vector_norm(vectors) / time_delta)
    return np.where(spd != np.nan, spd, 0.1)


def direction_vectors(tracking: np.ndarray):
    return tracking[1:, :2] - tracking[:-1, :2]


def compute_normals(vectors: np.ndarray):
    # Cross product on 0, 0, 1 vec and x, y, 0 vec (from the vectors)
    vectors[:, 2] = 0.0
    return np.linalg.cross(vectors, base_vecs[: vectors.shape[0]])[:, :2]
