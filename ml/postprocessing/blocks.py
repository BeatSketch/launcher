from typing import Literal
from ml.dtype import BeatSketchTrackingDataDetails
from ml.postprocessing import orientation
from util.ipc.decode import BeatSketchBlock
from util.map.dtype.beatmap import SaberHand


def generate(
    tracking: list[BeatSketchTrackingDataDetails],
    pred: list[bool],
    hand: Literal["left"] | Literal["right"],
):
    blocks: list[BeatSketchBlock] = []
    if len(tracking) != len(pred):
        print("Mismatched length!!")
        # TODO: Better handling of this
        # (tho this should never happen!)

    for i in range(min(len(tracking), len(pred))):
        if pred[i]:
            tracked = tracking[i]
            blocks.append(
                {
                    "beat": tracked["beat"],
                    "hand": SaberHand.RIGHT if hand == "right" else SaberHand.LEFT,
                    "orientation": orientation.determine_cut_direction(tracked),
                    "x": tracked["x"],
                    "y": tracked["y"],
                }
            )
    return blocks
