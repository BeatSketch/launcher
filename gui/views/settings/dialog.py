import PyQt6.QtWidgets as qt

from gui.elements import button, label
from gui.elements.dialog import open_msg_dialog
from gui.elements.dropdown import dropdown
from gui.elements.input import simple_input_widget
from util import config


def open_settings_dialog():
    """Open a dialog to configure BeatSketch"""
    # Basic setup
    dialog = qt.QDialog()
    dialog.setWindowTitle("Settings")

    container = qt.QVBoxLayout()

    # Title
    container.addLayout(label.centered_label("Settings", 25))

    # ── Configs ─────────────────────────────────────────────────────────
    # Inputs
    box = qt.QGridLayout()

    rx, get_rx = simple_input_widget()
    ry, get_ry = simple_input_widget()
    rz, get_rz = simple_input_widget()
    rx.setText(str(config.get_config()["saber_angle"]["x"]))
    ry.setText(str(config.get_config()["saber_angle"]["y"]))
    rz.setText(str(config.get_config()["saber_angle"]["z"]))
    global coll_enabled, dist_enabled, vibrate_enabled
    coll_enabled = False
    dist_enabled = False
    vibrate_enabled = False

    def update_dropdown_data(_):
        global coll_enabled, dist_enabled, vibrate_enabled
        coll_enabled = enable_collision_resolution.currentText() == "Enabled"
        dist_enabled = enable_distance_resolution.currentText() == "Enabled"
        vibrate_enabled = enable_vibrate.currentText() == "Enabled"

    enable_collision_resolution = dropdown(
        ["Enabled", "Disabled"], update_dropdown_data
    )
    enable_distance_resolution = dropdown(["Enabled", "Disabled"], update_dropdown_data)
    enable_vibrate = dropdown(["Enabled", "Disabled"], update_dropdown_data)

    box.addWidget(label.simple_label("Saber rotation around X axis"), 0, 0)
    box.addWidget(rx, 0, 1)
    box.addWidget(label.simple_label("Saber rotation around Y axis"), 1, 0)
    box.addWidget(ry, 1, 1)
    box.addWidget(label.simple_label("Saber rotation around Z axis"), 2, 0)
    box.addWidget(rz, 2, 1)
    box.addWidget(label.simple_label("Remove block collisions automatically"), 3, 0)
    box.addWidget(enable_collision_resolution, 3, 1)
    box.addWidget(label.simple_label("Remove too close blocks automatically"), 4, 0)
    box.addWidget(enable_distance_resolution, 4, 1)
    box.addWidget(label.simple_label("Enable Vibration"), 5, 0)
    box.addWidget(enable_vibrate, 5, 1)

    container.addLayout(box)

    # Controls
    def close_dialog():
        dialog.close()

    def save():
        config.update_rotation("x", get_rx())
        config.update_rotation("y", get_ry())
        config.update_rotation("z", get_rz())
        config.update_enabled_cleanup("collisions", coll_enabled)
        config.update_enabled_cleanup("distance", dist_enabled)
        config.update_vibrate(vibrate_enabled)
        config.save_config()
        open_msg_dialog("Settings saved")

    controls = qt.QHBoxLayout()
    controls.addWidget(button.create_button(close_dialog, "Close"))
    controls.addWidget(button.create_button(save, "Save"))

    container.addLayout(controls)

    dialog.setLayout(container)
    dialog.exec()
