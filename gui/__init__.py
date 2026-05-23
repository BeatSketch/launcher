from typing import Callable
import PyQt6.QtWidgets as qt

from gui.util import ident_func
from gui.views.home import home_view


def create_launcher_app(
    launch_func: Callable[[], None] = ident_func,
    testing_mode: bool = False,
    dev_mode: bool = False,
    vr_debug: bool = False,
):
    """Launcher start function. This actually opens the window

    Args:
        launch_func: A function to run once the VR application launches. Optional

    Returns:
        The Qt application and the window. Application can be used with close_window to kill the app
    """
    if testing_mode:
        print("TESTING MODE ACTIVE")
    if vr_debug:
        print("VR DEBUG MODE ACTIVE (print output of VR app)")

    # Create the main window
    app = qt.QApplication([])
    window = qt.QMainWindow()
    window.setWindowTitle("BeatSketch Launcher")

    # Wrap the home view
    wrapper = qt.QWidget()
    wrapper.setLayout(home_view(launch_func, testing_mode, dev_mode, vr_debug))
    window.setCentralWidget(wrapper)

    return app, window


def close_window(app: qt.QApplication):
    """Close the whole application

    Args:
        app: The Qt application object received from create_launcher_app
    """
    app.exit()
    exit(130)
