import sys
import time
import multiprocessing as mp

from generator import generate_training_data, get_no_block_share
from loader import load_replay_data
from tree import filesystem_walker
from util import write_cache

# TODO: Change this over
dir = sys.argv[1]

files = filesystem_walker(dir)


# TODO: Use folder instead of specific file and process all files in the specified folder
def process_file(file: str):
    start = time.time()
    data = load_replay_data(file)
    mid = time.time()
    training_data = generate_training_data(data[0], data[1], data[2])
    print(
        len(training_data),
        "datapoints were generated from this file, with no block share of",
        str(get_no_block_share(training_data) * 100) + "%",
    )
    print(
        "\n",
        "Processing took",
        time.time() - start,
        "with loading taking",
        mid - start,
        "and generating taking",
        time.time() - mid,
    )


for file in files:
    process_file(file)

# Make sure to leave this in to persist the cache and further reduce load on BeatSaver
write_cache()
