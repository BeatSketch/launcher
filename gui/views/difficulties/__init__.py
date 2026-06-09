from typing import Callable
from gui.elements import button
from gui.elements.dropdown import dropdown, update_dropdown
from gui.views.difficulties.new_difficulty_dialog import open_new_difficulty_dialog
import PyQt6.QtWidgets as qt

import map_handler.map as map_manager


def add_difficulty_controls(callback: Callable[[], None], testing_mode: bool = False):
    difficulty_controls = qt.QHBoxLayout()

    difficulty_controls.addWidget(
        button.create_button(
            lambda: open_new_difficulty_dialog(added_difficulty_handler, testing_mode),
            "Add difficulty",
        )
    )

    def added_difficulty_handler():
        d.setEnabled(True)
        difficulties = map_manager.get_map().list_beatmaps_with_difficulties()
        diff_list: list[str] = []
        for diff in difficulties:
            diff_list.append(f"{diff[0]} ({diff[1]})")

        update_dropdown(d, diff_list)

    def select_difficulty(_: str):
        idx = d.currentIndex()
        maps = map_manager.get_map().list_beatmaps()
        if idx > -1 and len(maps):
            map_manager.set_selected_difficulty(
                maps[idx]
            )
            callback()

    d = dropdown(["Please add a difficulty"], select_difficulty)
    d.setEnabled(False)
    difficulty_controls.addWidget(d)

    def new_map_loaded_handler():
        maps = map_manager.get_map().list_beatmaps()
        if len(maps) > 0:
            d.setEnabled(True)
            update_dropdown(d, maps)
            return True
        else:
            d.setEnabled(False)
            update_dropdown(d, ["Please add a difficulty"])
            return False

    # TODO: Edit button for details (of both difficulty and map)
    # TODO: Remove edit button again when new map is loaded

    return (difficulty_controls, new_map_loaded_handler)
