from typing import Callable

from PyQt6.QtWidgets import QComboBox


def dropdown(options: list[str], callback: Callable[[str], None]):
    """Create a dropdown

    Args:
        options: The dropdown options
        callback: Callback that is called when the selected item changes

    Returns:
        The dropdown
    """
    d, _ = simple_dropdown(options)

    d.currentTextChanged.connect(callback)

    return d


def simple_dropdown(options: list[str]):
    d = QComboBox()
    d.addItems(options)

    def get_value():
        return d.currentText()

    return d, get_value


def update_dropdown(dropdown: QComboBox, options: list[str]):
    dropdown.clear()
    dropdown.addItems(options)
