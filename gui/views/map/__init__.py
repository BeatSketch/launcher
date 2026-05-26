from typing import Callable
from gui.elements import button
from gui.elements.file_picker import directory_select_button
from gui.views.map.new_map_dialog import open_new_map_dialog
import PyQt6.QtWidgets as qt
import gui.elements.dialog as dialog


def add_map_controls(
    map_select_callback: Callable[[], None], testing_mode: bool = False
):
    map_controls = qt.QHBoxLayout()
    map_controls.addWidget(
        button.create_button(
            lambda: open_new_map_dialog(map_select_callback, testing_mode),
            "Create new map",
        )
    )
    map_controls.addWidget(
        directory_select_button(load_map, "Select the map", "Open existing map")
    )

    return map_controls


def load_map(map: str):
    if map != "":
        print("fixme: load the map", map)
        dialog.open_msg_dialog("This operation is not yet supported")
    else:
        dialog.open_msg_dialog("No map selected")
