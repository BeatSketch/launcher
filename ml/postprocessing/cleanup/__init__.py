from numpy import moveaxis

from ml.dtype import (
    BeatSketchPredictions as _BeatSketchPredictions,
    BeatSketchTrackingData as _BeatSketchTrackingData,
)
from ml.postprocessing.cleanup import (
    collisions as _collisions,
    converter as _converter,
    impossible_hits as _impossible_hits,
)
from util.dtype import BeatSketchBlock as _BeatSketchBlock
from ml.postprocessing.cleanup.config import enable_impossible_hit_cleanup


def clean_up_classifier_output(
    tracking: _BeatSketchTrackingData,
    pred: _BeatSketchPredictions,
    blocks: list[_BeatSketchBlock],
    dev_mode: bool = False,
) -> list[_BeatSketchBlock]:
    """Cleans up the map using heuristics, removing impossible to slice structures that the
    classifier may generate. Features can be enabled, disabled and configured in the config file

    Args:
        tracking: The tracking data in the intermediary format
        pred: The predictions for this data
        blocks: The blocks that were generated from the data

    Returns:
        The blocks, with the issues resolved
    """
    # Order matters:
    data = _converter.to_cleanup_format(tracking, pred, blocks)

    if dev_mode:
        print("Number of blocks pre cleanup", len(blocks))

    # 1. collisions
    try:
        data = _collisions.solve(data)
    except Exception as e:
        print("WARN: Collision removal has failed")
        if dev_mode:
            raise e

    # 2. impossible hits
    if enable_impossible_hit_cleanup:
        try:
            data = _impossible_hits.solve(data)
            if dev_mode:
                print(
                    "Number of data points after impossible hit cleanup",
                    len(data["left"]) + len(data["right"]),
                )
        except Exception as e:
            print("WARN: Impossible hit removal has failed")
            if dev_mode:
                raise e

    # 3. hand mixups
    # 4. Flow
    # The idea is to chain these into one another
    if dev_mode:
        print("Cleanup completed")

    converted = _converter.to_blocks(data)
    return converted
    # return _converter.to_blocks(data)
