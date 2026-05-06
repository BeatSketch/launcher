from typing import Callable

from PyQt6.QtWidgets import QPushButton


def create_button(
    callback: Callable[[], None],
    button_text: str = "Press me!",
):
    """Create a button with click callback

    Args:
        callback: The function to be executed on button click
        button_text: The text for the button

    Returns:
        The QPushButton
    """
    button = QPushButton()
    button.setText(button_text)
    button.pressed.connect(callback)
    return button
