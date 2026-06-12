from typing import Callable
from gui.elements import dialog
from util import config
from map_handler.map import BeatSaberMap
from map_handler.vr_manager import start_vr_app


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

    conf = config.get_config()
    args = [
        f'song="{map.get_audio_file()}"',
        f"bpm={map.get_bpm()}",
        f"rx={conf['saber_angle']['x']}",
        f"ry={conf['saber_angle']['y']}",
        f"rz={conf['saber_angle']['z']}",
        f"njs={njs}",
        f"mirror={'true' if conf['mirror'] else 'false'}"
        f"vibrate={'true' if conf['vibrate'] else 'false'}",
    ]

    if testing_mode:
        args = ["dev=true"]

    launch_func()

    def launch_status_handler(status: int):
        if status == 254:
            dialog.open_msg_dialog(
                "VR App is already running",
                title="VR Application already running",
            )
        elif status != 0:
            dialog.open_msg_dialog(
                "The VR Application has failed to launch. Exit code: " + str(status),
                title="Launching VR Application failed",
            )

    status, proc = start_vr_app(
        args,
        map,
        beatmap_name,
        config.get_config()["used_model"],
        debug=vr_debug,
        dev_mode=dev_mode,
    )

    if proc and status:
        proc.exit_code.connect(launch_status_handler)
    else:
        launch_status_handler(254)
