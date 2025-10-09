from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from ui.widgets.chat_view import ChatView
from ui.assistant_ui import Ui_AssistantPage
from core.gpt_assistant import GptAssistant

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
        emptyIcon.setPixmap(QPixmap(":resources/images/chatbot.png").scaled(340,340, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        emptyLabel = QLabel("Mình là trợ lý ảo của ChiTiêu+\nMình có thể giúp bạn trả lời các câu hỏi về quản lý chi tiêu.\nHãy bắt đầu trò chuyện với mình nhé!")
        emptyLabel.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        emptyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emptyLabel.setStyleSheet("color: gray")

        emptyLayout.addWidget(emptyIcon)
        emptyLayout.addWidget(emptyLabel)
        emptyLayout.addStretch()

        self.ui.chatView = ChatView()

        self.ui.chatContainer.addWidget(self.ui.emptyChatWidget)
        self.ui.chatContainer.addWidget(self.ui.chatView)

        self.ui.chatView.pushMessage("Chào bạn! Mình là trợ lý ảo của ChiTiêu+. Mình có thể giúp gì cho bạn?", isUserMessage=False)
        self.ui.chatView.pushMessage("Hãy nhập câu hỏi của bạn vào ô bên dưới và nhấn gửi nhé!", isUserMessage=False)
        self.ui.chatView.pushMessage("Bạn có thể hỏi mình về các chủ đề như:\n- Quản lý chi tiêu cá nhân\n- Lập kế hoạch tài chính\n- Mẹo tiết kiệm tiền\n- Phân tích thói quen chi tiêu\n- Cách sử dụng ứng dụng ChiTiêu+", isUserMessage=False)
        self.ui.chatContainer.setCurrentWidget(self.ui.chatView)

        self._gptAssistant = GptAssistant()
        # self._gptAssistant.addTransactionManager(self._transactionManager)

        self.ui.inputTbox.returnPressed.connect(self.onInputReturnPressed)

    def onInputReturnPressed(self):
        message = self.ui.inputTbox.text().strip()
        if message == "":
            return
        self.ui.inputTbox.clear()
        self.ui.chatView.pushMessage(message, isUserMessage=True)
        response = "Nfefef" # self._gptAssistant.sendMessage(message)
        self.ui.chatView.pushMessage(response, isUserMessage=False)
        self.ui.chatView.verticalScrollBar().setValue(self.ui.chatView.verticalScrollBar().maximum())
        
        




