from app.ui.home import HomeWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    window = HomeWindow()
    window.show()
    app.exec()