from typing import Callable
import PyQt6.QtWidgets as qt
from gui.elements.button import create_button
from gui.elements.file_picker import directory_picker, file_picker
from gui.elements.input import input_widget
from util.launch import BeatSketchSelectedFileList, launch_wrapper


def ident_func():
    pass


def create_config_interface(launch_func: Callable[[], None] = ident_func):
    def set_file(path: str, kind: str):
        if path == "":
            return
        files[kind] = path

    box = qt.QVBoxLayout()
    files: BeatSketchSelectedFileList = {"save": "", "cover": "", "song": ""}

    song_name, get_song = input_widget("Song name")
    song_artist, get_artist = input_widget("Song artist")
    mapper, get_mapper = input_widget("Mapper names")
    bpm, get_bpm = input_widget("BPM")
    njs, get_njs = input_widget("NJS")

    # TODO: Actually do what the label says, or remove it
    # possible library https://github.com/tinytag/tinytag
    note = qt.QLabel()
    note.setText(
        "When you select an audio file, we will attempt to find a title and artist in the metadata"
    )
    box.addWidget(note)
    box.addLayout(file_picker("Audio file", lambda x: set_file(x, "song")))
    box.addLayout(bpm)
    box.addLayout(njs)
    box.addLayout(song_name)
    box.addLayout(song_artist)
    box.addLayout(mapper)
    # TODO: Preview window (start and duration)

    box.addLayout(
        file_picker(
            "Cover Art",
            lambda x: set_file(x, "cover"),
            filter="Supported image formats (*.jpg *.jpeg)",
        )
    )

    box.addLayout(directory_picker("Map save directory", lambda x: set_file(x, "save")))

    box.addWidget(
        create_button(
            lambda: launch_wrapper(
                get_song(),
                get_artist(),
                get_mapper(),
                get_bpm(),
                get_njs(),
                files,
                launch_func,
            ),
            "Record map",
        )
    )

    return box
