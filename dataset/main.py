import sys
import time

from generator import generate_training_data
from loader import load_replay_data
from util import write_cache

file = sys.argv[1]


# TODO: Use folder instead of specific file and process all files in the specified folder
def process_file(file: str):
    start = time.time()
    data = load_replay_data(file)
    mid = time.time()
    print(generate_training_data(data[0], data[1], data[2]))
    print(
        "\n",
        "Processing took",
        time.time() - start,
        "with loading taking",
        mid - start,
        "and generating taking",
        time.time() - mid,
    )


process_file(file)

# Make sure to leave this in to persist the cache and further reduce load on BeatSaver
write_cache()
