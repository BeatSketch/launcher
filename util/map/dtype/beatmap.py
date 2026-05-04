from enum import Enum
from typing import TypedDict


class SaberHand(Enum):
    LEFT = 0
    RIGHT = 1


class CutDirection(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP_LEFT = 4
    UP_RIGHT = 5
    DOWN_LEFT = 6
    DOWN_RIGHT = 7
    ANY = 8


class BeatMapData(TypedDict):
    version: str
    bpmEvents: list[BeatMapBPMEvent]
    colorNotes: list[BeatMapColorNote]


class BeatMapBPMEvent(TypedDict):
    """BPM change events

    Attributes:
        b: beats since start
        m: The BPM to set
    """

    b: int
    m: int


# FIXME: b may need to be set to float (very likely)
class BeatMapColorNote(TypedDict):
    """The blocks to be placed

    Attributes:
        b: The beat at which to set
        x: The lane number (0 - 3)
        y: The layer number (0 - 3)
        c: The hand used for the slice
        d: The cut direction
    """

    b: int
    x: int
    y: int
    c: SaberHand
    d: CutDirection
