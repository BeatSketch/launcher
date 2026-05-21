from typing import Callable
from PyQt6.QtGui import QFont
import PyQt6.QtWidgets as qt
import PyQt6.QtCore as qtcore

from gui.config import create_config_interface, ident_func


def create_launcher_app(launch_func: Callable[[], None] = ident_func, testing_mode: bool = False):
    """Launcher start function. This actually opens the window

    Args:
        launch_func: A function to run once the VR application launches. Optional

    Returns:
        The Qt application and the window. Application can be used with close_window to kill the app
    """
    if testing_mode:
        print("TESTING MODE ACTIVE")

    app = qt.QApplication([])
    window = qt.QMainWindow()
    window.setWindowTitle("BeatSketch Launcher")

    box = qt.QVBoxLayout()

    title_wrapper = qt.QHBoxLayout()
    title_wrapper.setAlignment(qtcore.Qt.AlignmentFlag.AlignCenter)
    t = qt.QLabel()
    t.setText("BeatSketch Launcher")
    t.setFont(QFont("sans", 40))
    title_wrapper.addWidget(t)
    box.addLayout(title_wrapper)

    box.addLayout(create_config_interface(launch_func, testing_mode=testing_mode))

    wrapper = qt.QWidget()
    wrapper.setLayout(box)
    window.setCentralWidget(wrapper)

    return app, window


def close_window(app: qt.QApplication):
    """Close the whole application

    Args:
        app: The Qt application object received from create_launcher_app
    """
    app.exit()
    exit(130)
