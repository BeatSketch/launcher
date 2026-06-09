import PyQt6.QtWidgets as qt

from gui.elements import button, label
from gui.elements.dropdown import dropdown
from gui.elements.input import simple_input_widget


def open_settings_dialog():
    """Open a dialog to configure BeatSketch"""
    # Basic setup
    dialog = qt.QDialog()
    dialog.setWindowTitle("Settings")

    container = qt.QVBoxLayout()

    # Title
    container.addLayout(label.centered_label("Create new map", 20))

    # ── Configs ─────────────────────────────────────────────────────────

    # Inputs
    box = qt.QGridLayout()

    rx, get_rx = simple_input_widget()
    ry, get_ry = simple_input_widget()
    rz, get_rz = simple_input_widget()
    coll_enabled = False
    dist_enabled = False
    enable_collision_resolution = dropdown(["Enabled", "Disabled"], lambda val: ((coll_enabled := (val == "Enabled")), None)[-1])
    enable_distance_resolution = dropdown(["Enabled", "Disabled"])

    box.addWidget(label.simple_label("Song name"), 0, 0)
    box.addWidget(rx, 0, 1)
    box.addWidget(label.simple_label("Song name"), 0, 0)
    box.addWidget(ry, 0, 1)
    box.addWidget(label.simple_label("Song name"), 0, 0)
    box.addWidget(rz, 0, 1)
    box.addWidget(label.simple_label("Song name"), 0, 0)
    box.addWidget(enable_collision_resolution, 0, 1)
    box.addWidget(label.simple_label("Song name"), 0, 0)
    box.addWidget(enable_distance_resolution, 0, 1)


    container.addLayout(box)

    # Controls
    def close_dialog():
        dialog.close()

    def save():
        pass

    controls = qt.QHBoxLayout()
    controls.addWidget(button.create_button(close_dialog, "Cancel"))
    controls.addWidget(button.create_button(save, "Save"))

    container.addLayout(controls)

    dialog.setLayout(container)
    dialog.exec()
