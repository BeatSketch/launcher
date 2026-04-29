from typing import Callable
from PyQt5.QtGui import QFont
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtcore

from gui.button import create_button
from gui.file_picker import directory_picker, file_picker
from gui.input import input_widget


# NOTE: Likely going to use the return of the UI application
# (we should probably close it when the VR app launches)
# We can then re-launch the GUI when the VR app exits (except user hits exit to desktop in VR?)
def launch_launcher(launch: Callable[[list[str]], None]):
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

    # TODO: Actually do that, or remove this
    note = qt.QLabel()
    note.setText(
        "When you select an audio file, we will attempt to find a title and artist in the metadata"
    )
    box.addWidget(note)
    box.addLayout(file_picker("Audio file", lambda x: print("file", x)))

    # Config
    song_name = input_widget("Song name")
    song_artist = input_widget("Song artist")
    mapper = input_widget("Mapper names")
    bpm = input_widget("BPM")
    box.addLayout(song_name)
    box.addLayout(song_artist)
    box.addLayout(mapper)
    box.addLayout(bpm)
    # TODO: Preview window (start and duration)
    # TODO: Save location for the map
    box.addLayout(
        directory_picker("Map save directory", lambda x: print("Map directory", x))
    )
    box.addLayout(file_picker("Cover Art", lambda x: print("Cover art", x)))

    # TODO: Pass in the args and other data
    box.addWidget(create_button(lambda: launch([]), "Record map"))

    wrapper = qt.QWidget()
    wrapper.setLayout(box)
    window.setCentralWidget(wrapper)

    window.show()

    return app.exec()
