from ml.dtype import HANDS, BeatSketchTrackingData
from ml.preprocessing import BEAT_SPLIT, TRACKING_PER_UNIT
from ml.preprocessing.locations import hit_locations
from util.ipc.decode import BeatSketchVRData
import math
import numpy as np


def prepare(
    data: list[BeatSketchVRData], bpm: int, njs: float
) -> BeatSketchTrackingData:
    processed: BeatSketchTrackingData = {"left": [], "right": []}
    sec_per_unit = 60 / (bpm * BEAT_SPLIT)

    # Determine which time unit each data point belongs to
    buckets: dict[int, tuple[list[int], list[int]]] = {}
    for idx, frame in enumerate(data):
        for i, hand in enumerate(HANDS):
            time = int(
                (frame[hand]["timestamp"] + frame[hand]["pos"][2] / njs) / sec_per_unit
            )
            try:
                buckets[time][i].append(idx)
            except Exception:
                buckets[time] = ([], [])
                buckets[time][i].append(idx)

    for unit in range(len(buckets)):
        bucket = buckets[unit]
        for i, indices in enumerate(bucket):
            # Limit the number of data points used
            hand = "left" if i == 0 else "right"
            one_every_n_els = len(indices) / TRACKING_PER_UNIT
            els: list[np.ndarray] = []

            if len(indices) < TRACKING_PER_UNIT:
                print(
                    f"WARNING: Skipped data points filled in with {TRACKING_PER_UNIT - len(indices)} 0s"
                )
                for _ in range(TRACKING_PER_UNIT - len(indices)):
                    els.append(np.array([0, 0, 0]))

            for k in range(min(TRACKING_PER_UNIT, len(indices))):
                els.append(data[indices[math.floor(one_every_n_els * k)]][hand]["tip"])

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
