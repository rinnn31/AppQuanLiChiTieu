from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QMargins

from app.ui.home_ui import Ui_MainWindow
from app.ui.overview import OverviewPage
from app.utils.window_helper import install_dragging, install_drop_shadow

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setContentsMargins(QMargins(5,5,5,5))
        install_dragging(self, self.ui.titlePanel)
        install_drop_shadow(self.ui.windowWidget, radius=5)

        self.ui.closeBtn.clicked.connect(lambda: self.close())
        self.ui.closeBtn.enterEvent

        overview_page = OverviewPage(self)
        self.ui.pageContainer.layout().addWidget(overview_page)
        overview_page.show()

        
