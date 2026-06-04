from gui.elements.file_picker import directory_select_button, file_picker_button
from map_handler.dtype import BeatSketchSelectedFileList
import PyQt6.QtWidgets as qt


def files_inputs():
    files: BeatSketchSelectedFileList = {"save": "", "cover": "", "song": ""}

    def set_file(path: str, kind: str):
        if path == "":
            return
        files[kind] = path

    # Pickers
    file_pickers = qt.QHBoxLayout()
    file_pickers.addWidget(
        file_picker_button(
            lambda x: set_file(x, "song"),
            picker_text="Select audio file",
            button_text="Audio File",
        )
    )
    file_pickers.addWidget(
        file_picker_button(
            lambda x: set_file(x, "cover"),
            "Image files (*.png)",
            "Select the Cover art",
            "Cover Art",
        )
    )
    file_pickers.addWidget(
        directory_select_button(
            lambda x: set_file(x, "save"),
            "Select save folder for map",
            "Map folder",
        )
    )

    def get_files():
        return files

    return file_pickers, get_files
