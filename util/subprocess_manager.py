import multiprocessing as mp
from util.ipc import BeatSketchVRApplication

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
    com = BeatSketchVRApplication(args)
    while True:
        data = com.get_data()
        if isinstance(data, dict):
            print(com.parse_data(data))
        elif data == "proc:has-quit":
            print("\n\nEXITING SUBPROCESS\n\n")
            return
        # TODO: Instruction to jump back to earlier time (maybe not explicitly needed)
