from PyQt5 import QtWidgets

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addStretch(1)

