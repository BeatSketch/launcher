from typing import Callable, TypedDict
from gui.elements import dialog
from util.map import BeatSaberMap
from util.vr_manager import start_vr_app


class BeatSketchSelectedFileList(TypedDict):
    song: str
    save: str
    cover: str


def launch_wrapper(
    map: BeatSaberMap,
    beatmap_name: str,
    launch_func: Callable[[], None],
    testing_mode: bool = False,
    dev_mode: bool = False,
    vr_debug: bool = False,
):
    """A convenience wrapper for the VR app launch procedure.

    Args:
        map: The map to update
        beatmap_name: The name of the beatmap to update / create
        launch_func: A function to run before the launch happens
        testing_mode: Whether to enable testing mode (no required input in UI)
        vr_debug: Whether to enable debug mode for the VR app (prints output from it)
    """

    njs = map.get_njs(beatmap_name)

    # TODO: Load rotation offsets for sabers from config
    args = [
        f'song="{map.get_audio_file()}"',
        f"bpm={map.get_bpm()}",
        f"rx={0}",
        f"ry={0}",
        f"rz={0}",
        f"njs={njs}",
    ]
    if testing_mode:
        args = []

    launch_func()

    # TODO: Handle existing maps
    def launch_status_handler(status: int):
        if status != 0:
            dialog.open_msg_dialog(
                "The VR Application has failed to launch. Exit code: " + str(status),
                title="Launching VR Application failed",
            )

    # TODO: Load model from config
    status, proc = start_vr_app(
        args, map, beatmap_name, "mlp", debug=vr_debug, dev_mode=dev_mode
    )

    if proc and status:
        proc.exit_code.connect(launch_status_handler)
    else:
        launch_status_handler(254)
