from map_handler.ml.dtype import DATASET, HANDS, BeatSketchTrackingData
import numpy as np


def generate_model_readable_data(
    data: BeatSketchTrackingData,
) -> DATASET:
    """Convert the BeatSketchTrackingData into a format usable by the models

    Args:
        data: The TrackingData to convert

    Returns:
        Model-compatible data format
    """
    processed: tuple[list[np.ndarray], list[np.ndarray]] = ([], [])
    for hand_idx, hand in enumerate(HANDS):
        details_list = data[hand]
        for details in details_list:
            tracking = details["tracking"]
            dataset_frame: list[float] = [details["x"], details["y"], details["beat"]]
            for point in tracking:
                dataset_frame += point.tolist()

            processed[hand_idx].append(np.array(dataset_frame))

    return np.array(processed[0]), np.array(processed[1])
