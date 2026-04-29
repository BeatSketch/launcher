from typing import get_args
import PyQt5.QtWidgets as qt
from gui.elements.button import create_button
from gui.elements.file_picker import directory_picker, file_picker
from gui.elements.input import input_widget
from util.subprocess_manager import start_vr_app


def create_config_interface():
    box = qt.QVBoxLayout()
    files = {"save": "", "cover": "", "song": ""}

    def set_file(path: str, kind: str):
        files[kind] = path

    song_name, get_song = input_widget("Song name")
    song_artist, get_artist = input_widget("Song artist")
    mapper, get_mapper = input_widget("Mapper names")
    bpm, get_bpm = input_widget("BPM")

    # TODO: Actually do that, or remove this
    note = qt.QLabel()
    note.setText(
        "When you select an audio file, we will attempt to find a title and artist in the metadata"
    )
    box.addWidget(note)
    box.addLayout(file_picker("Audio file", lambda x: set_file(x, "song")))

    box.addLayout(song_name)
    box.addLayout(song_artist)
    box.addLayout(mapper)
    box.addLayout(bpm)
    # TODO: Preview window (start and duration)
    # TODO: Save location for the map
    box.addLayout(
        file_picker(
            "Cover Art",
            lambda x: set_file(x, "cover"),
            filter="Supported image formats (*.jpg *.jpeg)",
        )
    )
    box.addLayout(directory_picker("Map save directory", lambda x: set_file(x, "save")))

    # TODO: Pass in the args and other data
    box.addWidget(
        create_button(
            lambda: launch_wrapper(
                get_song(), get_artist(), get_mapper(), get_bpm(), files
            ),
            "Record map",
        )
    )

    return box


def launch_wrapper(
    song_name: str, song_artist: str, mapper: str, bpm: str, files: dict[str, str]
):
    if (
        files["song"] == ""
        or files["cover"] == ""
        or files["save"] == ""
        or song_name == ""
        or song_artist == ""
        or mapper == ""
    ):
        # TODO: Err msg, same checks also for other params
        return print("Missing config")

    print(files)
    start_vr_app([f'"{files["song"]}"'])
