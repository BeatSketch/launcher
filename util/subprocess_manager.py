import multiprocessing as mp
from util.ipc.decode import BeatSketchInstanceDataDecoder

global proc
proc: None | mp.Process = None


def start_vr_app(args: list[str]):
    global proc
    if proc and proc.is_alive():
        return False

    proc = mp.Process(target=_run, args=(args,))
    proc.start()
    return True


def _run(args: list[str]):
    com = BeatSketchInstanceDataDecoder(args)
    while True:
        print(com.get_data())
