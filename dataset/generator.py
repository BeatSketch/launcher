import time
from dtype import BeatSketchBlock, BeatSketchTrackingData, BeatSketchTrainingData
import math

GRID_FIELD_WIDTH = 0.5
GRID_FIELD_HEIGHT = 0.5

# Into how mnay parts to split each beat (should be power of 2 and no more than 8)
# I do also think we should make this configurable for the user? (or provide 2 settings?)
# Or at least for the training data, make it depend on the BPM
BEAT_SPLIT = 4
# Number of tracking data points per time unit
TRACKING_PER_UNIT = 5

# How many of the datapoints before to include
DATA_SLACK_BEFORE = 4
# How many of the datapoints after to include
DATA_SLACK_AFTER = 4


def generate_training_data(
    tracking: list[BeatSketchTrackingData], blocks: list[BeatSketchBlock], bpm: int
) -> list[BeatSketchTrainingData]:
    training_data: list[BeatSketchTrainingData] = []
    sec_per_unit = 60 / (bpm * BEAT_SPLIT)

    # Determine buckets for tracking data
    buckets_tracking: list[int] = []
    bucket_end = sec_per_unit
    for idx, frame in enumerate(tracking):
        if frame["time"] > bucket_end:
            buckets_tracking.append(idx)
            bucket_end += sec_per_unit
    buckets_tracking.append(len(tracking) - 1)

    # Determine buckets for blocks
    buckets_blocks: list[int] = [0]
    bucket_end = sec_per_unit
    for idx, frame in enumerate(blocks):
        if frame["time"] > bucket_end:
            diff = frame["time"] - bucket_end
            while diff > sec_per_unit:
                # Need to add empty buckets
                diff -= sec_per_unit
                buckets_blocks.append(idx)
            buckets_blocks.append(idx)
            bucket_end += sec_per_unit
    buckets_blocks.append(len(blocks) - 1)

    # Compute the training data
    prev = 0
    for beat, end in enumerate(buckets_tracking):
        one_every_n_els = (end - prev) / TRACKING_PER_UNIT

        els: list[BeatSketchTrackingData] = []
        for i in range(TRACKING_PER_UNIT):
            els.append(tracking[prev + math.floor(one_every_n_els * i)])

        locs = determine_possible_locs(els)
        # TODO: Append the prev and after slack here
        for loc in locs:
            # Determine if in this beat, there is a block in loc
            is_hit_l = False
            is_hit_r = False
            for block_idx in range(buckets_blocks[beat], buckets_blocks[beat + 1]):
                if (
                    blocks[block_idx]["x"] == loc[0]
                    and blocks[block_idx]["y"] == loc[1]
                ):
                    if blocks[block_idx]["is_right_hand"]:
                        is_hit_r = True
                    else:
                        is_hit_l = True

                    if is_hit_r and is_hit_l:
                        break

            training_data.append(
                {
                    "is_right_hand": False,
                    "x": loc[0],
                    "y": loc[1],
                    "beat": beat,
                    "has_block": is_hit_l,
                    "tracking": els,
                }
            )
            training_data.append(
                {
                    "is_right_hand": True,
                    "x": loc[0],
                    "y": loc[1],
                    "beat": beat,
                    "has_block": is_hit_r,
                    "tracking": els,
                }
            )

        prev = end

    return training_data


def determine_possible_locs(
    tracking: list[BeatSketchTrackingData],
) -> list[tuple[int, int]]:
    # Compute which grid spots the controller tip touches
    coords: list[tuple[int, int]] = []
    for pos in tracking:
        hand = pos["left"]
        for line in range(3):
            for col in range(4):
                if (
                    hand[0] < -1 + (col + 1) * GRID_FIELD_WIDTH
                    and hand[0] > -1 + col * GRID_FIELD_WIDTH
                    and hand[1] < 0 + (line + 1) * GRID_FIELD_HEIGHT
                    and hand[1] > 0 + line * GRID_FIELD_HEIGHT
                ):
                    coords.append((0, 0))

    return coords


def filter_training_data(
    no_block_share: float, training_data: list[BeatSketchTrainingData]
) -> list[BeatSketchTrainingData]:
    no_block_idxs: list[int] = []

    for idx, d in enumerate(training_data):
        if not d["has_block"]:
            no_block_idxs.append(idx)

    print(
        "Share is", len(no_block_idxs) / len(training_data), "target is", no_block_share
    )

    return training_data
