from PySide6.QtWidgets import QMainWindow, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QMargins

from ui.home_ui import Ui_MainWindow
from ui.overview import OverviewPage
from ui.manager import ManagerPage
from ui.assistant import AssistantPage
from utils.window_helper import installWindowDragging, applyDropShadow
from core.transaction_manager import TransactionManager

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._transactionManager = TransactionManager()

        self.setup()
        self.onOverviewBtnClicked()

    def setup(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setContentsMargins(QMargins(5,5,5,5))
        installWindowDragging(self, self.ui.titlePanel)
        applyDropShadow(self.ui.windowWidget, radius=5)

        self.ui.closeBtn.clicked.connect(lambda: self.close())

        self._overviewPage = OverviewPage(self._transactionManager)
        self._managerPage = ManagerPage(self._transactionManager)
        self._assistantPage = AssistantPage(self._transactionManager)

        self.ui.pageContainer.addWidget(self._overviewPage)
        self.ui.pageContainer.addWidget(self._managerPage)
        self.ui.pageContainer.addWidget(self._assistantPage)

        self.ui.overviewBtn.clicked.connect(self.onOverviewBtnClicked)
        self.ui.managerBtn.clicked.connect(self.onManagerBtnClicked)
        self.ui.chatBtn.clicked.connect(self.onChatBtnClicked)

    def onManagerBtnClicked(self):
        self.navigatePage(1, "QUẢN LÝ", ":/resources/images/black_wallet.png")

    def onOverviewBtnClicked(self):
        self.navigatePage(0, "TỔNG QUAN", ":/resources/images/black_dashboard.png")
        self._overviewPage.refreshData()
    
    def onChatBtnClicked(self):
        self.navigatePage(2, "TRỢ LÝ ẢO", ":/resources/images/black_chatbot.png")

    def navigatePage(self, index, name, iconPath):
        if self.ui.pageContainer.currentIndex() == index + 1:
            return
        navigateBtns = self.ui.navigationPanel.findChildren(QPushButton)
        for btn in navigateBtns:
            btn.setProperty("selected", False)
        navigateBtns[index].setProperty("selected", True)
        for btn in navigateBtns:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            
        self.ui.pageNameLb.setText(name)
        self.ui.pageIconLb.setPixmap(QPixmap(iconPath).scaled(30,30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.ui.pageContainer.setCurrentIndex(index+1)

