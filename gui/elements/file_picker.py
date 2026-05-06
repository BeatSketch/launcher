from typing import Callable
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QPushButton


def file_picker_button(
    picked_file: Callable[[str], None],
    filter: str = "Supported audio (*.ogg, *.mp3, *.wav)",
    picker_text: str = "Select the song file",
    button_text: str = "Select File",
):
    """Create a file picker button, launches File Picker and calls callback on File pick

    Args:
        picked_file: Callback for the picked file
        filter: The filter to apply to the inputs. Needs to contain a *.<extension> type string
        picker_text: The text to display as the title of the file picker
        button_text: The text of the button that opens the picker

    Returns:
        A QPushButton that opens the file picker
    """

    def handler():
        filename, _ = QFileDialog.getOpenFileName(caption=picker_text, filter=filter)

        picked_file(filename)

    button = QPushButton()
    button.setText(button_text)
    button.pressed.connect(handler)
    return button


def file_picker(
    msg: str,
    picked_file: Callable[[str], None],
    filter: str = "Supported audio (*.ogg *.mp3)",
    picker_text: str = "Select the song file",
    button_text: str = "Select File",
):
    """Add a file picker button

    Args:
        msg: The message to display next to the button
        picked_file: Callback for the picked file
        filter: The filter to apply to the inputs. Needs to contain a *.<extension> type string
        picker_text: The text to display as the title of the file picker
        button_text: The text of the button that opens the picker

    Returns:
        A QHBoxLayout with the message label and file picker button inside of it
    """
    button = file_picker_button(picked_file, filter, picker_text, button_text)

    t = QLabel()
    t.setText(msg)

    # Wrap in a box layout to make it scale
    layout = QHBoxLayout()
    layout.addWidget(t)
    layout.addWidget(button)

    return layout


def directory_select_button(
    selected_dir: Callable[[str], None],
    picker_text: str = "Select the directory",
    button_text: str = "Select directory",
):
    """Create a file save dialog button, launches file save dialog

    Args:
        selected_dir: Callback for the picked file
        picker_text: The text to display as the title of the file picker
        button_text: The text of the button that opens the picker

    Returns:
        A QPushButton that opens the file save dialog
    """

    def handler():
        selected_dir(QFileDialog.getExistingDirectory(caption=picker_text))

    button = QPushButton()
    button.setText(button_text)
    button.pressed.connect(handler)
    return button


def directory_picker(
    msg: str,
    selected_dir: Callable[[str], None],
    picker_text: str = "Select the directory",
    button_text: str = "Select directory",
):
    """Add a directory picker button

    Args:
        msg: The message to display next to the button
        selected_dir: Callback for the picked directory
        picker_text: The text to display as the title of the file picker
        button_text: The text of the button that opens the picker

    Returns:
        A QHBoxLayout with the message label and file picker button inside of it
    """
    button = directory_select_button(selected_dir, picker_text, button_text)

    t = QLabel()
    t.setText(msg)

    # Wrap in a box layout to make it scale
    layout = QHBoxLayout()
    layout.addWidget(t)
    layout.addWidget(button)

    return layout
