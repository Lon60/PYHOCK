from PyQt5 import QtWidgets, QtCore, QtGui
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os


class EncryptWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EncryptWidget, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.file_to_encrypt_label = QtWidgets.QLabel("File to encrypt")
        self.file_to_encrypt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_to_encrypt_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.file_to_encrypt_edit = QtWidgets.QLineEdit()
        self.file_to_encrypt_edit.setMinimumWidth(200)
        self.file_to_encrypt_button = QtWidgets.QPushButton("Browse")

        self.folder_to_encrypt_label = QtWidgets.QLabel("Folder to encrypt")
        self.folder_to_encrypt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.folder_to_encrypt_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.folder_to_encrypt_edit = QtWidgets.QLineEdit()
        self.folder_to_encrypt_edit.setMinimumWidth(200)
        self.folder_to_encrypt_button = QtWidgets.QPushButton("Browse")

        self.key_save_location_label = QtWidgets.QLabel("Location to save the key")
        self.key_save_location_label.setAlignment(QtCore.Qt.AlignCenter)
        self.key_save_location_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.key_save_location_edit = QtWidgets.QLineEdit()
        self.key_save_location_edit.setMinimumWidth(200)
        self.key_save_location_button = QtWidgets.QPushButton("Browse")

        self.key_checkbox = QtWidgets.QCheckBox("Generate a new key")
        self.key_checkbox.setChecked(True)

        self.custom_key_label = QtWidgets.QLabel("Custom key (Optional)")
        self.custom_key_label.setAlignment(QtCore.Qt.AlignCenter)
        self.custom_key_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.custom_key_edit = QtWidgets.QLineEdit()
        self.custom_key_edit.setDisabled(True)

        self.encrypt_file_button = QtWidgets.QPushButton("Encrypt File")
        self.encrypt_file_button.clicked.connect(self.encrypt_file)

        self.encrypt_folder_button = QtWidgets.QPushButton("Encrypt Folder")
        self.encrypt_folder_button.clicked.connect(self.encrypt_folder)

        layout.addWidget(self.file_to_encrypt_label)
        layout.addWidget(self.file_to_encrypt_edit)
        layout.addWidget(self.file_to_encrypt_button)
        layout.addWidget(self.folder_to_encrypt_label)
        layout.addWidget(self.folder_to_encrypt_edit)
        layout.addWidget(self.folder_to_encrypt_button)
        layout.addWidget(self.key_save_location_label)
        layout.addWidget(self.key_save_location_edit)
        layout.addWidget(self.key_save_location_button)
        layout.addWidget(self.key_checkbox)
        layout.addWidget(self.custom_key_label)
        layout.addWidget(self.custom_key_edit)
        layout.addWidget(self.encrypt_file_button)
        layout.addWidget(self.encrypt_folder_button)

        self.file_to_encrypt_button.clicked.connect(self.browse_file)
        self.folder_to_encrypt_button.clicked.connect(self.browse_folder)
        self.key_save_location_button.clicked.connect(self.browse_location)
        self.key_checkbox.stateChanged.connect(self.toggle_custom_key)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            self.file_to_encrypt_edit.setText(file_name)

    def browse_folder(self):
        dir_name = QFileDialog.getExistingDirectory()
        if dir_name:
            self.folder_to_encrypt_edit.setText(dir_name)

    def browse_location(self):
        dir_name = QFileDialog.getExistingDirectory()
        if dir_name:
            self.key_save_location_edit.setText(dir_name)

    def toggle_custom_key(self, state):
        if state == QtCore.Qt.Checked:
            self.custom_key_edit.setDisabled(True)
        else:
            self.custom_key_edit.setDisabled(False)

    def encrypt_file(self):
        file_to_encrypt = self.file_to_encrypt_edit.text()
        key_save_location = self.key_save_location_edit.text()

        if not file_to_encrypt or not key_save_location:
            QMessageBox.warning(self, "Warning", "Please fill all the fields")
            return

        if self.key_checkbox.isChecked():
            key = Fernet.generate_key()
        else:
            key = self.custom_key_edit.text().encode()

        try:
            with open(file_to_encrypt, "rb") as file:
                data = file.read()

            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)

            with open(file_to_encrypt, "wb") as file:
                file.write(encrypted)

            with open(f"{key_save_location}/key.txt", "wb") as file:
                file.write(key)

            QMessageBox.information(self, "Success", "File encrypted successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def encrypt_folder(self):
        folder_to_encrypt = self.folder_to_encrypt_edit.text()
        key_save_location = self.key_save_location_edit.text()

        if not folder_to_encrypt or not key_save_location:
            QMessageBox.warning(self, "Warning", "Please fill all the fields")
            return

        if self.key_checkbox.isChecked():
            key = Fernet.generate_key()
        else:
            key = self.custom_key_edit.text().encode()

        try:
            # Iterate over all files in the folder and its subfolders
            for root, dirs, files in os.walk(folder_to_encrypt):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    # Check if the path is a file
                    if os.path.isfile(file_path):
                        with open(file_path, "rb") as file:
                            data = file.read()

                        fernet = Fernet(key)
                        encrypted = fernet.encrypt(data)

                        with open(file_path, "wb") as file:
                            file.write(encrypted)

            with open(f"{key_save_location}/key.txt", "wb") as file:
                file.write(key)

            QMessageBox.information(self, "Success", "Folder encrypted successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
