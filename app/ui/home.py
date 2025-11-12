from PySide6.QtWidgets import QMainWindow, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QMargins

from app.ui.home_ui import Ui_MainWindow
from app.ui.overview import OverviewPage
from app.ui.manager import ManagerPage
from app.ui.assistant import AssistantPage
from app.utils.window_helper import installWindowDragging, applyDropShadow

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        # Khởi tạo các trang con và thêm vào bộ chứa trang
        self._overviewPage = OverviewPage()
        self._managerPage = ManagerPage()
        self._assistantPage = AssistantPage()

        self.ui.pageContainer.addWidget(self._overviewPage)
        self.ui.pageContainer.addWidget(self._managerPage)
        self.ui.pageContainer.addWidget(self._assistantPage)

        # Kết nối tín hiệu bấm nút điều hướng với các hàm xử lý
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
        # Nếu đã ở trang hiện tại thì không làm gì cả
        if self.ui.pageContainer.currentIndex() == index + 1:
            return
        
        # Lấy danh sách các nút điều hướng và cập nhật trạng thái chọn
        navigateBtns = self.ui.navigationPanel.findChildren(QPushButton)
        for btn in navigateBtns:
            btn.setProperty("selected", False)
        navigateBtns[index].setProperty("selected", True)
        
        # Refresh lại style để áp dụng thay đổi
        for btn in navigateBtns:
            btn.style().unpolish(btn)
            btn.style().polish(btn) 
            
        # Cập nhật tiêu đề trang và biểu tượng, sau đó chuyển đến trang tương ứng
        self.ui.pageNameLb.setText(name)
        self.ui.pageIconLb.setPixmap(QPixmap(iconPath).scaled(30,30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.ui.pageContainer.setCurrentIndex(index+1)

