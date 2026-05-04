from util.map.dtype.beatmap import BeatMapData, CutDirection, SaberHand
import json


class BeatMap:
    _data: BeatMapData

    def __init__(self, bpm) -> None:
        self._data = {
            "version": "3.0.0",
            "bpmEvents": [{"b": 0, "m": bpm}],
            "colorNotes": [],
        }

    def save(self, path):
        with open(path, "w") as file:
            file.write(json.dumps(self._data))

    def add_block(
        self, beat: int, x: int, y: int, hand: SaberHand, direction: CutDirection
    ):
        """Add a block to the beatmap

        Args:
            beat: The beat on which the block should be added
            x: The lane to use (0 - 3)
            y: The layer to use (0 - 3)
            hand: The hand that was used
            direction: The direction in which the block was cut
        """
        self._data["colorNotes"].append(
            {"b": beat, "x": x, "y": y, "c": hand, "d": direction}
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
