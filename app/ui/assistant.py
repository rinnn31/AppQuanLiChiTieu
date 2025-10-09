from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from ui.widgets.chat_view import ChatView
from ui.assistant_ui import Ui_AssistantPage

class AssistantPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AssistantPage()
        self.ui.setupUi(self)
        
        self.ui.emptyChatWidget = QWidget()
        emptyLayout = QVBoxLayout(self.ui.emptyChatWidget)
        emptyLayout.setContentsMargins(0,80,0,0)
        emptyLayout.setSpacing(30)

        emptyIcon = QLabel()
        emptyIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emptyIcon.setPixmap(QPixmap(":resources/images/chatbot.png").scaled(300,300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        emptyLabel = QLabel("Mình là trợ lý ảo của ChiTiêu+\nMình có thể giúp bạn trả lời các câu hỏi về quản lý chi tiêu.\nHãy bắt đầu trò chuyện với mình nhé!")
        emptyLabel.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        emptyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emptyLabel.setStyleSheet("color: gray")

        emptyLayout.addWidget(emptyIcon)
        emptyLayout.addWidget(emptyLabel)
        emptyLayout.addStretch()

        
        




