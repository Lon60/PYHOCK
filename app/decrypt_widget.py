from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os
from cryptography.fernet import Fernet

class DecryptWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DecryptWidget, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        self.file_to_decrypt_label = QtWidgets.QLabel("File to decrypt")
        self.file_to_decrypt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_to_decrypt_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.file_to_decrypt_edit = QtWidgets.QLineEdit()
        self.file_to_decrypt_edit.setMinimumWidth(200)
        self.file_to_decrypt_button = QtWidgets.QPushButton("Browse")

        self.folder_to_decrypt_label = QtWidgets.QLabel("Folder to decrypt")
        self.folder_to_decrypt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.folder_to_decrypt_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.folder_to_decrypt_edit = QtWidgets.QLineEdit()
        self.folder_to_decrypt_edit.setMinimumWidth(200)
        self.folder_to_decrypt_button = QtWidgets.QPushButton("Browse")

        self.key_label = QtWidgets.QLabel("Key")
        self.key_label.setAlignment(QtCore.Qt.AlignCenter)
        self.key_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.key_edit = QtWidgets.QLineEdit()

        self.decrypt_file_button = QtWidgets.QPushButton("Decrypt File")
        self.decrypt_file_button.clicked.connect(self.decrypt_file)

        self.decrypt_folder_button = QtWidgets.QPushButton("Decrypt Folder")
        self.decrypt_folder_button.clicked.connect(self.decrypt_folder)

        layout.addWidget(self.file_to_decrypt_label)
        layout.addWidget(self.file_to_decrypt_edit)
        layout.addWidget(self.file_to_decrypt_button)
        layout.addWidget(self.folder_to_decrypt_label)
        layout.addWidget(self.folder_to_decrypt_edit)
        layout.addWidget(self.folder_to_decrypt_button)
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_edit)
        layout.addWidget(self.decrypt_file_button)
        layout.addWidget(self.decrypt_folder_button)

        self.file_to_decrypt_button.clicked.connect(self.browse_file)
        self.folder_to_decrypt_button.clicked.connect(self.browse_folder)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            self.file_to_decrypt_edit.setText(file_name)

    def browse_folder(self):
        dir_name = QFileDialog.getExistingDirectory()
        if dir_name:
            self.folder_to_decrypt_edit.setText(dir_name)

    def decrypt_file(self):
        file_to_decrypt = self.file_to_decrypt_edit.text()
        key = self.key_edit.text().encode()

        if not file_to_decrypt or not key:
            QMessageBox.warning(self, "Warning", "Please fill all the fields")
            return

        try:
            with open(file_to_decrypt, 'rb') as file:
                data = file.read()

            fernet = Fernet(key)
            decrypted = fernet.decrypt(data)

            with open(file_to_decrypt, 'wb') as file:
                file.write(decrypted)

            QMessageBox.information(self, "Success", "File decrypted successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def decrypt_folder(self):
        folder_to_decrypt = self.folder_to_decrypt_edit.text()
        key = self.key_edit.text().encode()

        if not folder_to_decrypt or not key:
            QMessageBox.warning(self, "Warning", "Please fill all the fields")
            return

        try:
            # Iterate over all files in the folder and its subfolders
            for root, dirs, files in os.walk(folder_to_decrypt):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    # Check if the path is a file
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as file:
                            data = file.read()

                        fernet = Fernet(key)
                        decrypted = fernet.decrypt(data)

                        with open(file_path, 'wb') as file:
                            file.write(decrypted)

            QMessageBox.information(self, "Success", "Folder decrypted successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
