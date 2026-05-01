from typing import Callable
import PyQt5.QtWidgets as qt
from gui.elements.button import create_button
from gui.elements.file_picker import directory_picker, file_picker
from gui.elements.input import input_widget
from util.subprocess_manager import start_vr_app


def ident_func():
    pass


def create_config_interface(launch_func: Callable[[], None] = ident_func):
    def set_file(path: str, kind: str):
        if path == "":
            return
        files[kind] = path

    box = qt.QVBoxLayout()
    files = {"save": "", "cover": "", "song": ""}

    song_name, get_song = input_widget("Song name")
    song_artist, get_artist = input_widget("Song artist")
    mapper, get_mapper = input_widget("Mapper names")
    bpm, get_bpm = input_widget("BPM")

    # TODO: Actually do what the label says, or remove it
    note = qt.QLabel()
    note.setText(
        "When you select an audio file, we will attempt to find a title and artist in the metadata"
    )
    box.addWidget(note)
    box.addLayout(file_picker("Audio file", lambda x: set_file(x, "song")))
    box.addLayout(
        file_picker(
            "Cover Art",
            lambda x: set_file(x, "cover"),
            filter="Supported image formats (*.jpg *.jpeg)",
        )
    )

    box.addLayout(song_name)
    box.addLayout(song_artist)
    box.addLayout(mapper)
    box.addLayout(bpm)
    # TODO: Preview window (start and duration)

    box.addLayout(directory_picker("Map save directory", lambda x: set_file(x, "save")))

    box.addWidget(
        create_button(
            lambda: launch_wrapper(
                get_song(), get_artist(), get_mapper(), get_bpm(), files, launch_func
            ),
            "Record map",
        )
    )

    return box


def launch_wrapper(
    song_name: str,
    song_artist: str,
    mapper: str,
    bpm: str,
    files: dict[str, str],
    launch_func: Callable[[], None],
):
    # TODO: Decide which ones are mandatory
    if (
        files["song"] == ""
        or files["cover"] == ""
        or files["save"] == ""
        or song_name == ""
        or song_artist == ""
        or mapper == ""
        or bpm == ""
    ):
        # TODO: Err msg, same checks also for other params
        # TODO: More elaborate checks
        # return 
        print("Missing config")

    # TODO: Decide on args / data sent to VR (can adjust here,
    # the args are passed in as in the array there)
    launch_func()
    start_vr_app([f'song="{files["song"]}"', f"bpm={bpm}"])
