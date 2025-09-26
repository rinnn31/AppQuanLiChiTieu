from PySide6.QtWidgets import QMainWindow
class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        from app.ui.home_ui import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)