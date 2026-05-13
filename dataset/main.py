import sys

from generator import generate_training_data
from util import write_cache

file = sys.argv[1]

# TODO: Use folder instead of specific file and process all files in the specified folder
generate_training_data(file)

# Make sure to leave this in to persist the cache and further reduce load on BeatSaver
write_cache()
