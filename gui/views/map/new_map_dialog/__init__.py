from typing import Callable
import PyQt6.QtWidgets as qt

from gui.elements import button, label
from gui.elements.input import simple_input_widget
from gui.views.map.new_map_dialog.files import files_inputs
from map_handler import map as map_manager


def open_new_map_dialog(
    new_map_handler: Callable[[], None],
    testing_mode: bool = False,
):
    """Open a dialog to configure a new map

    Args:
        new_map_handler:
            Handler function for the newly created map. Its args are:
                - Song name
                - Artist name
                - Mapper name
                - BPM
                - Audio file
                - Cover art file
                - Save path (i.e. where to save the map to)
        testing_mode: Wheter or not to enable testing mode
    """
    # Basic setup
    dialog = qt.QDialog()
    dialog.setWindowTitle("BeatSketch Launcher: New Map")

    container = qt.QVBoxLayout()

    # Title
    container.addLayout(label.centered_label("Create new map", 20))

    # ── Configs ─────────────────────────────────────────────────────────
    container.addWidget(
        label.simple_label("NOTE: Only .ogg and .egg Vorbis Audio files are supported")
    )
    file_pickers, get_files = files_inputs()
    container.addLayout(file_pickers)

    # Inputs
    box = qt.QGridLayout()
    song_name, get_song = simple_input_widget()
    song_artist, get_artist = simple_input_widget()
    mapper, get_mapper = simple_input_widget()
    bpm, get_bpm = simple_input_widget()

    box.addWidget(label.simple_label("Song name"), 0, 0)
    box.addWidget(song_name, 0, 1)
    box.addWidget(label.simple_label("Artist name"), 1, 0)
    box.addWidget(song_artist, 1, 1)
    box.addWidget(label.simple_label("Mapper"), 2, 0)
    box.addWidget(mapper, 2, 1)
    box.addWidget(label.simple_label("BPM"), 3, 0)
    box.addWidget(bpm, 3, 1)

    container.addLayout(box)

    # Controls
    def close_dialog():
        dialog.close()

    def create_handler():
        files = get_files()
        if map_manager.new_map(
            get_song(), get_artist(), get_bpm(), get_mapper(), files, testing_mode
        ):
            new_map_handler()
            dialog.close()

    controls = qt.QHBoxLayout()
    controls.addWidget(button.create_button(close_dialog, "Cancel"))
    controls.addWidget(button.create_button(create_handler, "Create map"))

    container.addLayout(controls)

    dialog.setLayout(container)
    dialog.exec()
