from PyQt6.QtGui import QFont
import PyQt6.QtWidgets as qt
import PyQt6.QtCore as qtcore


def title():
    # Title widget
    title_wrapper = qt.QHBoxLayout()
    title_wrapper.setAlignment(qtcore.Qt.AlignmentFlag.AlignCenter)
    t = qt.QLabel()
    t.setText("BeatSketch Launcher")
    t.setFont(QFont("sans", 40))
    title_wrapper.addWidget(t)

    return title_wrapper
