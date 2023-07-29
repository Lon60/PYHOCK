from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from cryptography.fernet import Fernet
import qdarkstyle
import qtmodern.styles
import qtmodern.windows

class EncryptWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EncryptWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)

        self.file_to_encrypt_label = QtWidgets.QLabel("File to encrypt")
        self.file_to_encrypt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_to_encrypt_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.file_to_encrypt_edit = QtWidgets.QLineEdit()
        self.file_to_encrypt_edit.setMinimumWidth(200)
        self.file_to_encrypt_button = QtWidgets.QPushButton("Browse")

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

        self.encrypt_button = QtWidgets.QPushButton("Encrypt File")
        self.encrypt_button.clicked.connect(self.encrypt_file)

        layout.addWidget(self.file_to_encrypt_label)
        layout.addWidget(self.file_to_encrypt_edit)
        layout.addWidget(self.file_to_encrypt_button)
        layout.addWidget(self.key_save_location_label)
        layout.addWidget(self.key_save_location_edit)
        layout.addWidget(self.key_save_location_button)
        layout.addWidget(self.key_checkbox)
        layout.addWidget(self.custom_key_label)
        layout.addWidget(self.custom_key_edit)
        layout.addWidget(self.encrypt_button)

        self.file_to_encrypt_button.clicked.connect(self.browse_file)
        self.key_save_location_button.clicked.connect(self.browse_location)
        self.key_checkbox.stateChanged.connect(self.toggle_custom_key)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            self.file_to_encrypt_edit.setText(file_name)

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
            with open(file_to_encrypt, 'rb') as file:
                data = file.read()

            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)

            with open(file_to_encrypt, 'wb') as file:
                file.write(encrypted)

            with open(f"{key_save_location}/key.txt", 'wb') as file:
                file.write(key)

            QMessageBox.information(self, "Success", "File encrypted successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class DecryptWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DecryptWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)

        self.file_to_decrypt_label = QtWidgets.QLabel("File to decrypt")
        self.file_to_decrypt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_to_decrypt_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.file_to_decrypt_edit = QtWidgets.QLineEdit()
        self.file_to_decrypt_edit.setMinimumWidth(200)
        self.file_to_decrypt_button = QtWidgets.QPushButton("Browse")

        self.key_label = QtWidgets.QLabel("Key")
        self.key_label.setAlignment(QtCore.Qt.AlignCenter)
        self.key_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.key_edit = QtWidgets.QLineEdit()
        self.key_edit.setMinimumWidth(200)

        self.decrypt_button = QtWidgets.QPushButton("Decrypt File")
        self.decrypt_button.clicked.connect(self.decrypt_file)

        layout.addWidget(self.file_to_decrypt_label)
        layout.addWidget(self.file_to_decrypt_edit)
        layout.addWidget(self.file_to_decrypt_button)
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_edit)
        layout.addWidget(self.decrypt_button)

        self.file_to_decrypt_button.clicked.connect(self.browse_file)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            self.file_to_decrypt_edit.setText(file_name)

    def decrypt_file(self):
        file_to_decrypt = self.file_to_decrypt_edit.text()
        key = self.key_edit.text()

        if not file_to_decrypt or not key:
            QMessageBox.warning(self, "Warning", "Please fill all the fields")
            return

        try:
            with open(file_to_decrypt, 'rb') as file:
                data = file.read()

            fernet = Fernet(key.encode())
            decrypted = fernet.decrypt(data)

            with open(file_to_decrypt, 'wb') as file:
                file.write(decrypted)

            QMessageBox.information(self, "Success", "File decrypted successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class GenerateKeyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GenerateKeyWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)

        self.generate_button = QtWidgets.QPushButton("Generate Key")
        self.generate_button.clicked.connect(self.generate_key)

        self.key_label = QtWidgets.QLabel()
        self.key_label.setAlignment(QtCore.Qt.AlignCenter)
        self.key_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        self.copy_button = QtWidgets.QPushButton("Copy Key")
        self.copy_button.clicked.connect(self.copy_key)
        self.copy_button.setDisabled(True)

        layout.addWidget(self.generate_button)
        layout.addWidget(self.key_label)
        layout.addWidget(self.copy_button)

    def generate_key(self):
        key = Fernet.generate_key()
        self.key_label.setText(key.decode())
        self.copy_button.setDisabled(False)

    def copy_key(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.key_label.text())
        QMessageBox.information(self, "Success", "Key copied to clipboard")

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, app, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.app = app

        layout = QtWidgets.QVBoxLayout(self)

        self.light_mode_checkbox = QtWidgets.QCheckBox("Light mode")
        self.light_mode_checkbox.stateChanged.connect(self.toggle_light_mode)

        layout.addWidget(self.light_mode_checkbox)

    def toggle_light_mode(self, state):
        if state == QtCore.Qt.Checked:
            qtmodern.styles.light(self.app)
        else:
            qtmodern.styles.dark(self.app)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()

        self.app = app
        qtmodern.styles.dark(self.app)

        # Create the dropdown menu
        self.menu = QtWidgets.QComboBox()
        self.menu.addItem("Encrypt")
        self.menu.addItem("Decrypt")
        self.menu.addItem("Generate Key")
        self.menu.addItem("Settings")
        self.menu.currentIndexChanged.connect(self.update_ui)

        # Create the stacked widget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(EncryptWidget())
        self.stacked_widget.addWidget(DecryptWidget())
        self.stacked_widget.addWidget(GenerateKeyWidget())
        self.stacked_widget.addWidget(SettingsWidget(self.app))

        # Create the main layout
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.menu)
        top_layout.addStretch()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.stacked_widget)

        # Create the main widget and set the main layout
        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(main_layout)

        # Set the main widget as the central widget
        self.setCentralWidget(main_widget)

        # Set the window title
        self.setWindowTitle("PYHOCK")

        # Create ModernWindow after setting central widget
        self.main_window = qtmodern.windows.ModernWindow(self)

        # Set the window to a fixed size
        self.setFixedSize(self.size())

    def update_ui(self, index):
        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)
    window.main_window.show()
    sys.exit(app.exec_())
