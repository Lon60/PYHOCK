from PyQt5 import QtWidgets, QtCore
from encrypt_widget import EncryptWidget
from decrypt_widget import DecryptWidget
from generate_key_widget import GenerateKeyWidget
from settings_widget import SettingsWidget
import sys
import app_styles

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.setWindowTitle("PYHOCK")
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(EncryptWidget())
        self.stacked_widget.addWidget(DecryptWidget())
        self.stacked_widget.addWidget(GenerateKeyWidget())
        self.stacked_widget.addWidget(SettingsWidget())

        self.menu_combo = QtWidgets.QComboBox()
        self.menu_combo.addItem("Encrypt")
        self.menu_combo.addItem("Decrypt")
        self.menu_combo.addItem("Generate Key")
        self.menu_combo.addItem("Settings")
        self.menu_combo.currentIndexChanged.connect(self.stacked_widget.setCurrentIndex)

        main_layout.addWidget(self.menu_combo)
        main_layout.addWidget(self.stacked_widget)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app_styles.apply_styles(app)
    mw = app_styles.create_modern_window(MainWindow(app))
    mw.show()
    sys.exit(app.exec_())
