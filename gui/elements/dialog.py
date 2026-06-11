from typing import Callable, TypedDict
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)


class DialogAction(TypedDict):
    name: str
    callback: Callable[[], None]
    close_dialog: bool


default_action: DialogAction = {
    "name": "Ok",
    "callback": lambda: None,
    "close_dialog": True,
}


def open_flexible_dialog(
    title: str, actions: list[DialogAction] = [default_action], msg: str = ""
):
    dialog = QDialog()
    dialog.setWindowTitle("BeatSketch Launcher")

    layout = QVBoxLayout()

    title_widget = QLabel()
    title_widget.setFont(QFont("sans", 30))
    title_widget.setText(title)
    layout.addWidget(title_widget)

    if msg != "":
        msg_widget = QLabel()
        msg_widget.setText(msg)
        layout.addWidget(msg_widget)

    if len(actions) > 0:
        actions_layout = QHBoxLayout()
        for action in actions:

            def cb():
                dialog.close()
                action["callback"]()

            button = QPushButton()
            button.setText(action["name"])
            button.pressed.connect(cb)
            actions_layout.addWidget(button)
        layout.addLayout(actions_layout)

    dialog.setLayout(layout)
    dialog.exec()


def open_msg_dialog(
    msg: str,
    actions: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok,
    title: str = ""
):
    dialog = QMessageBox()
    if title == "":
        dialog.setWindowTitle("BeatSketch Launcher")
    else:
        dialog.setWindowTitle(title)
    dialog.setText(msg)
    dialog.setStandardButtons(actions)

    dialog.exec()
