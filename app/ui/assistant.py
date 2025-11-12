from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt
from app.ui.widgets.chat_view import ChatView
from app.ui.assistant_ui import Ui_AssistantPage
from app.chatbot import ChattingService, BotAssistant

class AssistantPage(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_AssistantPage()
        self.ui.setupUi(self)

        # Khởi tạo giao diện sẽ hiện thị khi chưa có cuộc trò chuyện nào
        self._emptyChatWidget = QWidget()
        emptyLayout = QVBoxLayout(self._emptyChatWidget)
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

        self._chatView = ChatView()
       
        # Thiết lập chat container và đặt giao diện trống làm giao diện mặc định
        self.ui.chatContainer.addWidget(self._emptyChatWidget)
        self.ui.chatContainer.addWidget(self._chatView)
        self.ui.chatContainer.setCurrentWidget(self._emptyChatWidget)

        # Thiết lập dịch vụ trò chuyện với bot trợ lý ảo
        transactionManager = QApplication.instance().getTransactionManager()
        botAssistant = BotAssistant()
        botAssistant.setTransactionManager(transactionManager)
        self._chatService = ChattingService(botAssistant=botAssistant)
        self._chatService.messageReceived.connect(self.onResponseReceived)
        self._chatService.stateChanged.connect(self.onChattingStateChanged)

        self.ui.sendBtn.clicked.connect(self.onSendBtnClicked)
        self.ui.deleteBtn.clicked.connect(self.onDeleteChatBtnClicked)
        self.ui.inputTbox.returnPressed.connect(self.onInputEntered)

    def onInputEntered(self):
        # Kiểm tra trạng thái của nút gửi để tránh gửi nhiều yêu cầu cùng lúc
        if self.ui.sendBtn.property("state") == "busy":
            return
        message = self.ui.inputTbox.text().strip()
        if not message:
            return
        
        # Chuyển sang giao diện chat nếu đang ở giao diện trống
        if self.ui.chatContainer.currentWidget() == self._emptyChatWidget:
            self.ui.chatContainer.setCurrentWidget(self._chatView)

        # Gửi tin nhắn qua ChatService xử lí vào hiện thị trong ChatView
        self.ui.inputTbox.clear()
        self._chatView.pushMessage(message)
        self._chatService.sendMessage(message)

    def onSendBtnClicked(self):
        # Chuyển sang giao diện chat nếu đang ở giao diện trống
        if self.ui.chatContainer.currentWidget() == self._emptyChatWidget:
            self.ui.chatContainer.setCurrentWidget(self._chatView)

        message = self.ui.inputTbox.text().strip()
        if not message:
            # Nếu đang chờ phản hồi từ bot trợ lý ảo, hủy yêu cầu hiện tại
            if self.ui.sendBtn.property("state") == "busy":
                self._chatService.stopCurrentChatting()
            return
        
        self.ui.inputTbox.clear()
        self._chatView.pushMessage(message)
        self._chatService.sendMessage(message)
            
    def onChattingStateChanged(self, state: str):
        # Cập nhật trạng thái của nút gửi và giao diện chat dựa trên trạng thái hiện tại
        self.ui.sendBtn.setProperty("state", state)
        if state == "busy":
            self.ui.sendBtn.setIcon(QIcon(":/resources/images/white_square.png"))
            self._chatView.enableIncomeChattingState()
        elif state == "idle":
            self.ui.sendBtn.setIcon(QIcon(":/resources/images/white_up.png"))
            self._chatView.disableIncomeChattingState()

    def onResponseReceived(self, response: str):
        # Nhận tin nhắn phan hồi từ bot trợ lý ảo và hiển thị trong giao diện chat
        self._chatView.pushMessage(response.strip(), isOutgoingMessage=False)

    def onDeleteChatBtnClicked(self):
        # Xóa toàn bộ cuộc trò chuyện và hiển thị giao diện trống
        self._chatView.clearMessages()
        self.ui.chatContainer.setCurrentWidget(self._emptyChatWidget)