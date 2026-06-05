from map_handler.ml.dtype import HANDS, BeatSketchTrackingData
from map_handler.ml.preprocessing.values import BEAT_SPLIT, TRACKING_PER_UNIT
from map_handler.ml.preprocessing.hit_locations import hit_locations
from map_handler.dtype import BeatSketchVRData
import math
import numpy as np


def prepare(
    data: list[BeatSketchVRData], bpm: float, njs: float, dev_mode: bool = False
) -> BeatSketchTrackingData:
    """Convert the BeatSketchVRData into a more easily manageable format
    that is then further processed into other formats

    Args:
        data: The tracking data
        bpm: The BPM of the song
        njs: The Note Jump Speed of the song

    Returns:
        The converted tracking data.
    """
    processed: BeatSketchTrackingData = {"left": [], "right": [], "bpm": bpm}
    sec_per_unit = 60 / (bpm * BEAT_SPLIT)

    # Determine which time unit each data point belongs to
    buckets: dict[int, tuple[list[int], list[int]]] = {}
    for idx, frame in enumerate(data):
        for i, hand in enumerate(HANDS):
            beat = int(
                (frame[hand]["timestamp"] - frame[hand]["pos"][2] / njs) / sec_per_unit
            )
            try:
                buckets[beat][i].append(idx)
            except Exception:
                buckets[beat] = ([], [])
                buckets[beat][i].append(idx)

    for unit in range(len(buckets)):
        bucket: tuple[list[int], list[int]] = ([], [])
        try:
            bucket = buckets[unit]
        except KeyError:
            pass
        for i, indices in enumerate(bucket):
            # Limit the number of data points used
            hand = "left" if i == 0 else "right"
            one_every_n_els = len(indices) / TRACKING_PER_UNIT
            els: list[np.ndarray] = []

            if len(indices) < TRACKING_PER_UNIT:
                if dev_mode:
                    print(
                        f"WARNING: Data point filled in with {TRACKING_PER_UNIT - len(indices)} 0s"
                    )
                for _ in range(TRACKING_PER_UNIT - len(indices)):
                    els.append(np.array([0, 0, 0, 0, 0, 0, -1]))

            for k in range(min(TRACKING_PER_UNIT, len(indices))):
                loc = data[indices[math.floor(one_every_n_els * k)]][hand]
                els.append(np.concatenate((loc["tip"], loc["direction"], [loc["timestamp"]])))

            # Add the to be processed buckets
            hits = hit_locations(els)
            for hit in hits:
                processed[hand].append(
                    {
                        "beat": unit / BEAT_SPLIT,
                        "tracking": els,
                        "x": hit[0],
                        "y": hit[1],
                    }
                )

    return processed
