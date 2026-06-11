import PyQt6.QtWidgets as qt
from typing import Callable, cast
from gui.elements import button, label
from gui.elements.dropdown import simple_dropdown
from gui.elements.input import simple_input_widget
from map_handler import map as map_manager
from map_handler.map.dtype.info import DifficultyLevels


def open_new_difficulty_dialog(
    callback: Callable[[], None], testing_mode: bool = False
):
    dialog = qt.QDialog()
    dialog.setWindowTitle("BeatSketch Launcher: New Map")

    container = qt.QVBoxLayout()

    # Title
    box = qt.QGridLayout()
    container.addLayout(label.centered_label("Add difficulty", 20))

    # Inputs
    name, get_name = simple_input_widget()
    njs, get_njs = simple_input_widget()
    difficulty, get_difficulty = simple_dropdown(
        ["Easy", "Normal", "Hard", "Expert", "Expert+"]
    )

    box.addWidget(label.simple_label("Map name"), 1, 0)
    box.addWidget(name, 1, 1)
    box.addWidget(label.simple_label("Note Jump Speed"), 2, 0)
    box.addWidget(njs, 2, 1)
    box.addWidget(label.simple_label("Difficulty"), 3, 0)
    box.addWidget(difficulty, 3, 1)

    container.addLayout(box)

    # Controls
    def close_dialog():
        dialog.close()

    def create_handler():
        if map_manager.new_difficulty(
            get_name(),
            cast(DifficultyLevels, get_difficulty()),
            get_njs(),
            testing_mode,
        ):
            callback()
            dialog.close()

    controls = qt.QHBoxLayout()
    controls.addWidget(button.create_button(close_dialog, "Cancel"))
    controls.addWidget(button.create_button(create_handler, "Add difficulty"))
    container.addLayout(controls)

    dialog.setLayout(container)
    dialog.exec()
