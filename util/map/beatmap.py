from util.ipc.decode import BeatSketchBlock
from util.map.dtype.beatmap import BeatMapData, CutDirection, SaberHand
import json


class BeatMap:
    _data: BeatMapData

    def __init__(self, bpm: int) -> None:
        """Create a new BeatMap (data for the difficulty)

        Args:
            bpm: The BPM of the map
        """
        self._data = {
            "version": "3.0.0",
            "bpmEvents": [{"b": 0, "m": bpm}],
            "colorNotes": [],
        }

    def save(self, path: str):
        """Save the beatmap to the specified filepath

        Args:
            path: The path to save to
        """
        with open(path, "w") as file:
            file.write(json.dumps(self._data))

    def add_block(
        self, beat: int, x: int, y: int, hand: SaberHand, direction: CutDirection
    ):
        """Add a block to the beatmap

        Args:
            beat: The beat on which the block should be added
            x: The lane to use (0 - 3)
            y: The layer to use (0 - 2)
            hand: The hand that was used
            direction: The direction in which the block was cut
        """
        self._data["colorNotes"].append(
            {"b": beat, "x": x, "y": y, "c": hand, "d": direction}
        )

    def add_block_from_internal_block_type(self, block: BeatSketchBlock):
        self._data["colorNotes"].append(
            {
                "b": block["beat"],
                "x": block["x"],
                "y": block["y"],
                "c": block["hand"],
                "d": block["orientation"],
            }
        )

    def add_bpm_event(self, beat: int, bpm: int):
        """Add a BPM event to the beatmap

        Args:
            beat: The beat on which this happened
            bpm: The bpm to set
        """
        self._data["bpmEvents"].append({"b": beat, "m": bpm})

    def get_current_bpm(self) -> int:
        """Get the current BPM

        Returns:
            The current BPM
        """
        return self._data["bpmEvents"][len(self._data["bpmEvents"]) - 1]["m"]
