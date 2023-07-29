from PyQt5 import QtWidgets, QtCore, QtGui
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os
import qdarkstyle

class EncryptWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EncryptWidget, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        # File path input
        self.file_path_label = QtWidgets.QLabel("File to encrypt")
        self.file_path_label.setStyleSheet("QLabel { font-weight: bold; }")
        self.file_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_path_input = QtWidgets.QLineEdit()
        self.file_path_button = QtWidgets.QPushButton("Browse")
        self.file_path_button.clicked.connect(self.browse_file)

        # Key path input
        self.key_path_label = QtWidgets.QLabel("Key file path")
        self.key_path_label.setStyleSheet("QLabel { font-weight: bold; }")
        self.key_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.key_path_input = QtWidgets.QLineEdit()
        self.key_path_button = QtWidgets.QPushButton("Browse")
        self.key_path_button.clicked.connect(self.browse_key_directory)

        # Checkbox to determine whether to generate a key
        self.generate_key_checkbox = QtWidgets.QCheckBox("Generate key")
        self.generate_key_checkbox.setChecked(True)
        self.generate_key_checkbox.toggled.connect(self.toggle_key_entry)

        # Key input (disabled by default)
        self.key_input = QtWidgets.QLineEdit()
        self.key_input.setDisabled(True)

        # Encrypt button
        self.encrypt_button = QtWidgets.QPushButton("Encrypt File")
        self.encrypt_button.clicked.connect(self.encrypt_file)

        # Add widgets to layout
        layout.addWidget(self.file_path_label)
        layout.addWidget(self.file_path_input)
        layout.addWidget(self.file_path_button)
        layout.addWidget(self.key_path_label)
        layout.addWidget(self.key_path_input)
        layout.addWidget(self.key_path_button)
        layout.addWidget(self.generate_key_checkbox)
        layout.addWidget(self.key_input)
        layout.addWidget(self.encrypt_button)

    def browse_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_path_input.setText(file_path)

    def browse_key_directory(self):
        key_directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        if key_directory:
            self.key_path_input.setText(key_directory)

    def toggle_key_entry(self, checked):
        self.key_input.setDisabled(checked)

    def encrypt_file(self):
        file_path = self.file_path_input.text()
        key_path = self.key_path_input.text()
        generate_key = self.generate_key_checkbox.isChecked()

        if not os.path.isfile(file_path):
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid file path.")
            return

        if not os.path.isdir(key_path):
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid key file path.")
            return

        try:
            with open(file_path, "rb") as f:
                data = f.read()

            if generate_key:
                key = Fernet.generate_key()
            else:
                key = self.key_input.text().encode()

            cipher_suite = Fernet(key)
            encrypted_data = cipher_suite.encrypt(data)

            with open(file_path, "wb") as f:
                f.write(encrypted_data)

            with open(os.path.join(key_path, "key.txt"), "wb") as f:
                f.write(key)

            QtWidgets.QMessageBox.information(self, "Success", "File encrypted successfully.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", str(e))

class DecryptWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DecryptWidget, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        # File path input
        self.file_path_label = QtWidgets.QLabel("File to decrypt")
        self.file_path_label.setStyleSheet("QLabel { font-weight: bold; }")
        self.file_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_path_input = QtWidgets.QLineEdit()
        self.file_path_button = QtWidgets.QPushButton("Browse")
        self.file_path_button.clicked.connect(self.browse_file)

        # Key input
        self.key_input_label = QtWidgets.QLabel("Decryption key")
        self.key_input_label.setStyleSheet("QLabel { font-weight: bold; }")
        self.key_input_label.setAlignment(QtCore.Qt.AlignCenter)
        self.key_input = QtWidgets.QLineEdit()

        # Decrypt button
        self.decrypt_button = QtWidgets.QPushButton("Decrypt File")
        self.decrypt_button.clicked.connect(self.decrypt_file)

        # Add widgets to layout
        layout.addWidget(self.file_path_label)
        layout.addWidget(self.file_path_input)
        layout.addWidget(self.file_path_button)
        layout.addWidget(self.key_input_label)
        layout.addWidget(self.key_input)
        layout.addWidget(self.decrypt_button)

    def browse_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_path_input.setText(file_path)

    def decrypt_file(self):
        file_path = self.file_path_input.text()
        key = self.key_input.text().encode()

        if not os.path.isfile(file_path):
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid file path.")
            return

        try:
            with open(file_path, "rb") as f:
                data = f.read()

            cipher_suite = Fernet(key)
            decrypted = cipher_suite.decrypt(data)

            with open(file_path, "wb") as f:
                f.write(decrypted)

            QtWidgets.QMessageBox.information(self, "Success", "File decrypted successfully.")
        except InvalidToken:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid decryption key.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", str(e))

class GenerateKeyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GenerateKeyWidget, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        # Key display
        self.key_label = QtWidgets.QLabel("Generated key")
        self.key_display = QtWidgets.QLineEdit()
        self.key_display.setReadOnly(True)

        # Generate button
        self.generate_button = QtWidgets.QPushButton("Generate Key")
        self.generate_button.clicked.connect(self.generate_key)

        # Copy button
        self.copy_button = QtWidgets.QPushButton("Copy Key")
        self.copy_button.clicked.connect(self.copy_key)

        # Add widgets to layout
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_display)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.copy_button)

    def generate_key(self):
        key = Fernet.generate_key()
        self.key_display.setText(key.decode())

    def copy_key(self):
        clipboard = QtGui.QGuiApplication.clipboard()
        clipboard.setText(self.key_display.text())

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, app, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.app = app

        layout = QtWidgets.QVBoxLayout(self)

        # Dark mode checkbox
        self.dark_mode_checkbox = QtWidgets.QCheckBox("Dark mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)

        # Add widget to layout
        layout.addWidget(self.dark_mode_checkbox)

    def toggle_dark_mode(self, state):
        if state == QtCore.Qt.Checked:
            self.app.setStyleSheet(qdarkstyle.load_stylesheet())
        else:
            self.app.setStyleSheet("")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()

        self.app = app
        # Create a status bar
        self.statusBar()

        # Create a menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('PYHOCK')

        # Add options to the menu
        decryptAction = QtWidgets.QAction('Decrypt', self)
        decryptAction.triggered.connect(self.show_decrypt_widget)

        encryptAction = QtWidgets.QAction('Encrypt', self)
        encryptAction.triggered.connect(self.show_encrypt_widget)

        generateKeyAction = QtWidgets.QAction('Generate Key', self)
        generateKeyAction.triggered.connect(self.show_generate_key_widget)

        settingsAction = QtWidgets.QAction('Settings', self)
        settingsAction.triggered.connect(self.show_settings_widget)

        fileMenu.addAction(decryptAction)
        fileMenu.addAction(encryptAction)
        fileMenu.addAction(generateKeyAction)
        fileMenu.addAction(settingsAction)

        # Create the central widget
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Create the other widgets
        self.decrypt_widget = DecryptWidget()
        self.encrypt_widget = EncryptWidget()
        self.generate_key_widget = GenerateKeyWidget()
        self.settings_widget = SettingsWidget(self.app)

        # Add the widgets to the central widget
        self.central_widget.addWidget(self.decrypt_widget)
        self.central_widget.addWidget(self.encrypt_widget)
        self.central_widget.addWidget(self.generate_key_widget)
        self.central_widget.addWidget(self.settings_widget)

        # Show the encrypt widget by default
        self.show_encrypt_widget()

    def show_decrypt_widget(self):
        self.central_widget.setCurrentWidget(self.decrypt_widget)
        self.statusBar().showMessage('Decrypt')

    def show_encrypt_widget(self):
        self.central_widget.setCurrentWidget(self.encrypt_widget)
        self.statusBar().showMessage('Encrypt')

    def show_generate_key_widget(self):
        self.central_widget.setCurrentWidget(self.generate_key_widget)
        self.statusBar().showMessage('Generate Key')

    def show_settings_widget(self):
        self.central_widget.setCurrentWidget(self.settings_widget)
        self.statusBar().showMessage('Settings')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)
    window.setWindowFlags((window.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint) | QtCore.Qt.WindowCloseButtonHint)
    window.setFixedSize(window.size())
    window.show()
    sys.exit(app.exec_())