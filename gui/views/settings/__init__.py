from gui.elements import button
from gui.views.settings.dialog import open_settings_dialog


def add_settings_button():
    b = button.create_button(
        lambda: open_settings_dialog(),
        "Settings",
    )

    return b
