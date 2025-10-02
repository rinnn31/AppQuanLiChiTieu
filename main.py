from app.ui.home import HomeWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

if __name__ == "__main__":
    app = QApplication([])
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    screen = app.primaryScreen()
    size = screen.size()

    window = HomeWindow()
    window.resize(size * 0.8)
    window.show()
    app.exec()