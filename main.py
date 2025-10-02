from app.ui.home import HomeWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

if __name__ == "__main__":
    app = QApplication([])
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    window = HomeWindow()
    window.show()
    app.exec()