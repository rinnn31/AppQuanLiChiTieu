from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt
from ui.widgets.chat_view import ChatView
from ui.assistant_ui import Ui_AssistantPage
from core.bot_assistant import ChattingService, BotAssistant

class AssistantPage(QWidget):
    def __init__(self, transactionManager=None,parent=None):
        super().__init__(parent)
        self.ui = Ui_AssistantPage()
        self.ui.setupUi(self)
        
        self.emptyChatWidget = QWidget()
        emptyLayout = QVBoxLayout(self.emptyChatWidget)
        emptyLayout.setContentsMargins(0,80,0,0)
        emptyLayout.setSpacing(30)

        emptyIcon = QLabel()
        emptyIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emptyIcon.setPixmap(QPixmap(":resources/images/chatbot.png").scaled(340,340, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        emptyLabel = QLabel("Mình là trợ lý ảo của ChiTiêu+\nMình có thể giúp bạn trả lời các câu hỏi về quản lý chi tiêu.\nHãy bắt đầu trò chuyện với mình nhé!")
        emptyLabel.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        emptyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emptyLabel.setStyleSheet("color: gray")

        emptyLayout.addWidget(emptyIcon)
        emptyLayout.addWidget(emptyLabel)
        emptyLayout.addStretch()

        self.chatView = ChatView()

        self.ui.chatContainer.addWidget(self.emptyChatWidget)
        self.ui.chatContainer.addWidget(self.chatView)

        self.chatView.pushBotMessage("Chào bạn! Mình là trợ lý ảo của ChiTiêu+. Mình có thể giúp gì cho bạn?")
        self.chatView.pushBotMessage("Hãy nhập câu hỏi của bạn vào ô bên dưới và nhấn gửi nhé!")
        self.chatView.pushBotMessage("Bạn có thể hỏi mình về các chủ đề như:\n- Quản lý chi tiêu cá nhân\n- Lập kế hoạch tài chính\n- Mẹo tiết kiệm tiền\n- Phân tích thói quen chi tiêu\n- Cách sử dụng ứng dụng ChiTiêu+")
        self.ui.chatContainer.setCurrentWidget(self.chatView)

        botAssistant = BotAssistant()
        botAssistant.setTransactionManager(transactionManager)
        self._chatService = ChattingService(botAssistant=botAssistant)
        self._chatService.messageReceived.connect(self.onResponseReceived)
        self._chatService.stateChanged.connect(self.onChattingStateChanged)

        self.ui.sendBtn.clicked.connect(self.onSendBtnClicked)

    def onSendBtnClicked(self):
        message = self.ui.inputTbox.text().strip()
        if not message:
            if self.ui.sendBtn.property("state") == "busy":
                self._chatService.stopCurrentChatting()
            return
        
        self.ui.inputTbox.clear()
        self._chatService.sendMessage(message)
            
    def onChattingStateChanged(self, state: str):
        self.ui.sendBtn.setProperty("state", state)
        if state == "busy":
            self.ui.sendBtn.setIcon(QIcon(":/resources/images/white_square.png"))
            self.chatView.startBotChatting()
        elif state == "idle":
            self.ui.sendBtn.setIcon(QIcon(":/resources/images/white_up.png"))
            self.chatView.stopBotChatting()

    def onResponseReceived(self, response: str):
        self.chatView.pushBotMessage(response)


