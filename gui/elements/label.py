from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel
import PyQt6.QtCore as qtcore


def simple_label(text: str, font_size: int = -1, font_type: str = "sans"):
    t = QLabel()
    t.setText(text)

    if font_size > -1:
        t.setFont(QFont(font_type, font_size))
    else:
        if font_type != "sans":
            t.setFont(QFont(font_type))

    return t


def centered_label(text: str, font_size: int = -1, font_type: str = "sans"):
    t = simple_label(text, font_size, font_type)
    title_wrapper = QHBoxLayout()
    title_wrapper.setAlignment(qtcore.Qt.AlignmentFlag.AlignCenter)
    title_wrapper.addWidget(t)

    return title_wrapper
