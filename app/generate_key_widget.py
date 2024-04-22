from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet

class GenerateKeyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GenerateKeyWidget, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
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
