#!/usr/bin/env python3

from gui import launch_launcher
from util.ipc.decode import BeatSketchInstanceDataDecoder


def start_vr_app(args: list[str]):
    # TODO: Put this into separate process (multiprocessing lib likely, as load can get quite high depending on models).
    # Also, only allow one running instance at a time
    com = BeatSketchInstanceDataDecoder(args)

    # This is ofc not what we're going to do in the end, just for testing purposes
    while True:
        print(com.get_data())

# TODO: Controllers and stuff here;
# launch_ui is probably gonna get renamed and will take some args likely
launch_launcher(start_vr_app)
