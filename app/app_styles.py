from PyQt5 import QtWidgets
import qtmodern.styles
import qtmodern.windows

def apply_styles(app):
    qtmodern.styles.dark(app)

def create_modern_window(window):
    return qtmodern.windows.ModernWindow(window)
