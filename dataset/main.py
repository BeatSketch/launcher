from typing import Literal, TypedDict, cast
from bsor.Bsor import make_bsor
import quaternion
import numpy as np
import sys


class BeatSketchTrackingData(TypedDict):
    left: list[float]
    right: list[float]
    time: float


class BeatSketchTrainingData(TypedDict):
    left: list[float]
    right: list[float]
    time: float


class BeatSketchBlocks(TypedDict):
    orientation: int
    x: int
    y: int
    time: float
    is_right_hand: bool
    good_cut: bool


file = sys.argv[1]


# bpm = sys.argv[2]
# https://github.com/BeatLeader/BS-Open-Replay
# This is the replay format used
def generate_training_data(file: str, bpm: int):
    with open(file, "rb") as f:
        # TODO: Check if rotation is correct (or if controller offsets need to be computed)
        # bsor.controller_offsets.left - This is how to get the offsets if needed
        # I am almost certain this is correct
        bsor = make_bsor(f)

        # TODO: Figure out what the base vector is (unit vector in which direction?)
        # This is almost certainly correct
        base_vec = np.array([1, 0, 0])
        angle_comp_vec = base_vec

        # Discard map criteria
        if bsor.info.speed != 0:
            print("This map was played in practice mode -> Not suitable")
            exit(0)
        tracking_data: list[BeatSketchTrackingData] = []

        # for frame in bsor.frames:
        for frame in [bsor.frames[0]]:
            hand_l = frame.left_hand
            hand_r = frame.left_hand
            quat_l = quaternion.quaternion(
                hand_l.w_rot, hand_l.x_rot, hand_l.y_rot, hand_l.z_rot
            )
            quat_r = quaternion.quaternion(
                hand_r.w_rot, hand_r.x_rot, hand_r.y_rot, hand_r.z_rot
            )
            dir_l = quaternion.rotate_vectors(quat_l, base_vec)
            dir_r = quaternion.rotate_vectors(quat_r, base_vec)
            tip_l = dir_l + np.array(hand_l.position)
            tip_r = dir_r + np.array(hand_l.position)
            tracking_data.append(
                {
                    "left": cast(list[float], tip_l.tolist()),
                    "right": cast(list[float], tip_r.tolist()),
                    "time": frame.time,
                }
            )

        block_data: list[BeatSketchBlocks] = []
        bsor.notes.reverse()
        for block in bsor.notes:
            block.event_time
            block_data.append(
                {
                    "good_cut": False,
                    "is_right_hand": False,
                    "orientation": 0,
                    "time": 0,
                    "x": 0,
                    "y": 0,
                }
            )
            if block.cut:
                # Do cheapo projection (just setting the z axis to 0) to compute the cut angle using a [0, 1, 0] vector
                normal = np.array(block.cut.cutNormal)
                normal[2] = 0

                angle = np.arccos(normal.dot(angle_comp_vec) / (np.linalg.norm(normal))) / np.pi * 180
                # TODO: Positive / negative angle
                print(
                    "Block for hand",
                    block.colorType,
                    "normal",
                    block.cut.cutNormal,
                    "time",
                    block.event_time - block.cut.timeDeviation,
                    "angle",
                    angle,
                )
            else:
                print("Miss or bad cut")

        training_data: list[BeatSketchTrackingData] = []

        # TODO: Create dataset from the data


generate_training_data(file, 0)
