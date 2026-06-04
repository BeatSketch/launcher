from ml.postprocessing.cleanup.dtype import BeatSketchCleanupGroup

# import numpy as np


class Node:
    idx: int
    neighbours: list[Node]

    def __init__(self, idx: int) -> None:
        self.idx = idx


translation = [0, 4, 2, 6, 1, 7, 3, 5]
vecs = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]


def process(x: int, y: int, grid: list[list[int]], group: list[BeatSketchCleanupGroup]):
    # Use modified DFS to figure out if blocks can be hit
    def util(x: int, y: int, layer_changed: bool, orig_dir: int) -> list[int]:
        """V2
        If out of bounds, return bad
        For all three possible directions of cutting (if layer_changed is false), do
            If there is a block in the spot, do
                Call this func with new coordinates and layer changed if direction is not the same as curr block
        If there were multiple paths explored, do
            nothing
        """
        # TODO: Can we do anything about multiple valid paths?
        # The way the orientation algorithm works, there can't be any terribly stupid assignments,
        # so we do not need to check for bad orientations

        # If block is out of bounds, report that
        if x < 0 or x > 3 or y < 0 or y > 2:
            return []

        this_idx = grid[y][x]

        # If there is no block here, skip through
        if this_idx < 0:
            return util(x + vecs[orig_dir][0], y + vecs[orig_dir][1], False, orig_dir)

        dir = translation[group[this_idx]["block"]["orientation"].value]
        dirs = [(dir + 1) % 8, dir, (dir + 7) % 8]

        processed: list[int] = []
        for i, d in enumerate(dirs):
            if not (layer_changed and i != 1):
                processed += util(x + vecs[d][0], y + vecs[d][1], i != 1, d)

        return processed

    # TODO: Resolve issues with neighbouring blocks (pick the one closer to the slice path)
    # This may work automatically
    return util(
        x, y, False, translation[group[grid[y][x]]["block"]["orientation"].value]
    )
