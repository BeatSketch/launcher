from PyQt5.QtGui import QFont
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtcore

from gui.config import create_config_interface


# NOTE: Likely going to use the return of the UI application
# (we should probably close it when the VR app launches)
# We can then re-launch the GUI when the VR app exits (except user hits exit to desktop in VR?)
def create_launcher_app():
    # TODO: Theming, maybe using this: https://pypi.org/project/qt-themes/
    app = qt.QApplication([])
    window = qt.QMainWindow()
    window.setWindowTitle("BeatSketch Launcher")

    box = qt.QVBoxLayout()

    title_wrapper = qt.QHBoxLayout()
    # NOTE: Pyright may show this as error. It isn't.
    title_wrapper.setAlignment(qtcore.Qt.AlignCenter)
    t = qt.QLabel()
    t.setText("BeatSketch Launcher")
    t.setFont(QFont("sans", 40))
    title_wrapper.addWidget(t)
    box.addLayout(title_wrapper)

    box.addLayout(create_config_interface())

    wrapper = qt.QWidget()
    wrapper.setLayout(box)
    window.setCentralWidget(wrapper)

    return app, window


def close_window(app: qt.QApplication):
    print("KEYBOARD")
    app.exit()
