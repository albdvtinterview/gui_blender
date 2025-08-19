from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit,
    QFileDialog, QLabel, QComboBox, QFrame
)
from PySide6.QtCore import Slot
import subprocess
import json
import os

# TODO: сделать кросс-платформенный подбор пути
# TODO: переделать архитектуру создания и хранения новых скриптов
BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"  # path to blender ON MAC
BLENDER_GET_COLLECTIONS_SCRIPT_PATH = "src/scripts/blender/get_collection_names.py"
BLENDER_EXPORT_SCRIPT_PATH = "src/scripts/blender/export_collection_objects.py"
BLENDER_IMPORT_SCRIPT_PATH = "src/scripts/blender/import_fbx.py"
DEFAULT_DIRECTORY = os.path.expanduser("~/PycharmProjects/gui_blender/assets")
SCRIPT_TYPES = ["Import to Blender", "Export from Blender"]  # 0 1

# TODO: Плохая зависимость к пути проекта и его названия!
fbx_file_name = "test"
FBX_EXPORT_PATH = os.path.expanduser("~/PycharmProjects/gui_blender/assets/" + fbx_file_name + ".fbx")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # head widgets
        self.setWindowTitle("Main Window")
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.file_path = ""

        # widgets
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Path to .fbx file")
        self.add_path_button = QPushButton("Open")
        self.add_path_button.clicked.connect(self.on_file_dialog_open)
        self.run_script_button = QPushButton("Run script")
        self.run_script_button.clicked.connect(self.on_run_script)

        # ComboBox: Export / Import
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(SCRIPT_TYPES)
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)

        # ComboBox: Collections (blocked by default)
        self.label_for_collection = QLabel("Collection:")
        self.collections_combo = QComboBox()
        self.collections_combo.setPlaceholderText("Scene Collection")
        self.collections_combo.setEnabled(False)

        # layouts
        self.select_folder_layout = QHBoxLayout()
        self.select_folder_layout.addWidget(self.line_edit)
        self.select_folder_layout.addWidget(self.add_path_button)

        self.run_script_layout = QVBoxLayout()
        self.run_script_layout.addWidget(QLabel("Mode:"))
        self.run_script_layout.addWidget(self.mode_combo)
        self.run_script_layout.addWidget(QLabel("Path:"))
        self.run_script_layout.addLayout(self.select_folder_layout)
        self.run_script_layout.addWidget(self.label_for_collection)
        self.run_script_layout.addWidget(self.collections_combo)
        self.run_script_layout.addWidget(self.run_script_button)

        self.setLayout(self.run_script_layout)

    @Slot()
    def on_file_dialog_open(self):
        """Открытие диалога для выбора файла или папки"""
        # Определяем фильтр в зависимости от режима
        if self.mode_combo.currentText() == SCRIPT_TYPES[0]:  # Import
            self.file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select FBX file",
                DEFAULT_DIRECTORY,
                "FBX Files (*.fbx)"
            )
        else:  # Export
            self.file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select .blend file",
                DEFAULT_DIRECTORY,
                "Blend Files (*.blend)"
            )
        self.add_collections_to_combo_box()

    def add_collections_to_combo_box(self):
        self.line_edit.setText(self.file_path)
        self.line_edit.clearFocus()
        self.collections_combo.clear()

        if self.mode_combo.currentText() == SCRIPT_TYPES[1] and self.file_path.endswith(".blend"):
            self.collections_combo.setEnabled(True)
            collection_names = self.get_collections_in_blender_file()
            self.collections_combo.addItems(collection_names)
        else:
            self.collections_combo.setEnabled(False)

    def get_collections_in_blender_file(self) -> list[str]:
        """Текст"""
        try:
            command = [
                BLENDER_PATH,
                "-b", self.file_path,
                "-P", BLENDER_GET_COLLECTIONS_SCRIPT_PATH
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            stdout = result.stdout

            start_marker = "===BEGIN_JSON==="
            end_marker = "===END_JSON==="
            collection_names = []

            start = stdout.find(start_marker)
            end = stdout.find(end_marker)

            if start != -1 and end != -1:
                json_str = stdout[start + len(start_marker):end].strip()
                collection_names = json.loads(json_str)
            else:
                print("JSON not found in Blender output")
            return collection_names

        except Exception as e:
            print("Error running Blender:", e)
            return []

    @Slot()
    def on_mode_changed(self, text):
        """Срабатывает при смене режима Export/Import"""
        if text == SCRIPT_TYPES[1]:  # Export from Blender
            self.line_edit.setPlaceholderText("Path to .blend file")
            self.line_edit.clear()
            if self.line_edit.text().endswith(".blend"):
                self.collections_combo.setEnabled(True)
            else:
                self.collections_combo.setEnabled(False)
        if text == SCRIPT_TYPES[0]:  # Import to Blender
            self.line_edit.setPlaceholderText("Path to .fbx file")
            self.line_edit.clear()
            self.collections_combo.setEnabled(False)

    @Slot()
    def on_run_script(self):
        if self.mode_combo.currentText() == SCRIPT_TYPES[1]:  # Export from Blender
            print("Started exporting...")
            self.on_fxb_export_from_blender()
        if self.mode_combo.currentText() == SCRIPT_TYPES[0]:  # Import to Blender
            print("Started importing...")
            self.on_fbx_import_to_blender()

    def on_fbx_import_to_blender(self):
        # TODO: # тестовый .blend file path нужно убрать и сделать выбор через gui
        command = [
            BLENDER_PATH,
            "-b", f"{os.path.expanduser("~/PycharmProjects/gui_blender/assets/test.blend")}",
            "-P", BLENDER_IMPORT_SCRIPT_PATH,
            "--",
            self.file_path
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        stdout = result.stdout

        start_marker = "===BEGIN_JSON==="
        end_marker = "===END_JSON==="
        data = {}

        start = stdout.find(start_marker)
        end = stdout.find(end_marker)

        if start != -1 and end != -1:
            json_str = stdout[start + len(start_marker):end].strip()
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError as e:
                data = {"error": f"Failed to decode JSON: {e}"}
        else:
            data = {"error": "JSON not found in Blender output"}
        print(data)

    def on_fxb_export_from_blender(self):
        # Запускаем Blender и передаем аргументы
        command = [
            BLENDER_PATH,
            "-b", self.file_path,
            "-P", BLENDER_EXPORT_SCRIPT_PATH,
            "--",
            self.collections_combo.currentText(),
            FBX_EXPORT_PATH
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        stdout = result.stdout

        start_marker = "===BEGIN_JSON==="
        end_marker = "===END_JSON==="
        data = {}

        start = stdout.find(start_marker)
        end = stdout.find(end_marker)

        if start != -1 and end != -1:
            json_str = stdout[start + len(start_marker):end].strip()
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError as e:
                data = {"error": f"Failed to decode JSON: {e}"}
        else:
            data = {"error": "JSON not found in Blender output"}
        print(data)

