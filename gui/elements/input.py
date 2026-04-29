from typing import Callable
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


def input_widget(
    msg: str, max_length: int = 50
) -> tuple[QHBoxLayout, Callable[[], str]]:
    """Create a text input widget, with the message displayed left of it.
        It will auto-shrink and grow

    Args:
        msg: The message / description to display
        max_length: The max length of the input

    Returns:
        A QHBoxLayout that can be added to a layout with addLayout
    """
    le = simple_input_widget(max_length)

    t = QLabel()
    t.setText(msg)

    # Wrap in a box layout to make it scale
    layout = QHBoxLayout()
    layout.addWidget(t)
    layout.addWidget(le)

    def get_text():
        return le.text()

    return layout, get_text


def simple_input_widget(max_length: int = 50) -> QLineEdit:
    """Create a QLineEdit Widget (single line text input) widget
    with the default styling applied

    Args:
        max_length: The max length of the input

    Returns:
        A QLineEdit Widget. Add to a layout using addWidget
    """
    le = QLineEdit()
    le.setMaxLength(max_length)
    return le
