from typing import Callable
import PyQt6.QtWidgets as qt

from gui.elements import button
from gui.views.difficulties import add_difficulty_controls
from gui.views.map import add_map_controls
from gui.views.title import title
from map_handler import map as map_manager
from map_handler import launch_wrapper


def home_view(
    launch_func: Callable[[], None],
    testing_mode: bool = False,
    dev_mode: bool = False,
    vr_debug: bool = False,
):
    main_box = qt.QVBoxLayout()
    main_box.addLayout(title())

    controls_box = qt.QVBoxLayout()

    def select_complete_handler():
        start_button.setEnabled(True)

    difficulty, new_map_func = add_difficulty_controls(
        select_complete_handler, testing_mode
    )

    def map_selected_handler():
        # User will need to pick a difficulty in the dropdown
        controls_box.addLayout(difficulty)
        start_button.setEnabled(new_map_func())

    controls_box.addLayout(add_map_controls(map_selected_handler, testing_mode))
    main_box.addLayout(controls_box)

    # Start VR application button
    start_button = button.create_button(
        lambda: launch_wrapper(
            map_manager.get_map(),
            map_manager.get_selected_difficulty(),
            launch_func,
            testing_mode=testing_mode,
            dev_mode=dev_mode,
            vr_debug=vr_debug,
        ),
        "Record map",
    )
    start_button.setEnabled(False)
    main_box.addWidget(start_button)

    return main_box
