from PyQt5.QtGui import QFont
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtcore

from gui.file_picker import file_picker
from gui.input import input_widget


# NOTE: Likely going to use the return of the UI application 
# (we should probably close it when the VR app launches)
# We can then re-launch the GUI when the VR app exits (except user hits exit to desktop in VR?)
def launch_ui():
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

    box.addLayout(input_widget("Song name"))
    box.addLayout(input_widget("Song artist"))
    box.addLayout(file_picker("Audio file", lambda x: print("file", x)))

    wrapper = qt.QWidget()
    wrapper.setLayout(box)
    window.setCentralWidget(wrapper)

    window.show()

    return app.exec()
