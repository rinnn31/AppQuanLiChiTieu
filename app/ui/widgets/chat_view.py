from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QMovie

class ChatView(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.chatContainer = QWidget()
        self.chatContainer.setStyleSheet("background: white; margin: 0px;")
        self.chatLayout = QVBoxLayout(self.chatContainer)
        self.chatLayout.setContentsMargins(30,50,30,30)
        self.chatLayout.setSpacing(10)
        self.setWidget(self.chatContainer)
        self.setWidgetResizable(True)

    def pushUserMessage(self, message: str):
        messageItem = self._addMessageItem(isUserMessage=True)
        messageLb = messageItem.findChild(QLabel, "userMessageContent")
        messageLb.setText(message)

        self.chatContainer.adjustSize()
    
    def startBotChatting(self):
        if self.getBotTypingStateItem() is not None:
            return
        
        messageItem = self._addMessageItem(isUserMessage=False)
        messageLb = messageItem.findChild(QLabel, "botMessageContent")
        messageLb.setScaledContents(True)
        messageLb.setFixedSize(65, 40)
        movie = QMovie(":resources/gifs/typing.gif")
        movie.setSpeed(150)
        movie.setScaledSize(QSize(50, 30))
        messageLb.setProperty("isLoading", True)
        messageLb.setMovie(movie)
        movie.start()

        self.chatContainer.resize(self.chatContainer.width(), self.chatContainer.sizeHint().height())

    def stopBotChatting(self):
        typingStateItem = self.getBotTypingStateItem()
        if typingStateItem is not None:
            messageLb = typingStateItem.findChild(QLabel, "botMessageContent")
            movie = messageLb.movie()
            if movie is not None:
                movie.stop()
            typingStateItem.deleteLater()
        
        self.chatContainer.resize(self.chatContainer.width(), self.chatContainer.sizeHint().height())

    def getBotTypingStateItem(self) -> QHBoxLayout:
        for layoutIndex in range(self.chatLayout.count()-1, -1, -1):
            item = self.chatLayout.itemAt(layoutIndex).widget()
            if isinstance(item, QWidget):
                messageLb = item.findChild(QLabel, "botMessageContent")
                if messageLb and messageLb.property("isLoading"):
                    return item
        return None

    def pushBotMessage(self, message: str):
        self.stopBotChatting()
        messageItem = self._addMessageItem(isUserMessage=False)
        messageLb = messageItem.findChild(QLabel, "botMessageContent")
        messageLb.setText(message)

        self.chatContainer.resize(self.chatContainer.width(), self.chatContainer.sizeHint().height())   

    def _addMessageItem(self, isUserMessage: bool) -> QWidget:
        messageWidget = QWidget()
        messageLayout = QHBoxLayout(messageWidget)

        messageLb = QLabel()
        messageLb.setObjectName("userMessageContent" if isUserMessage else "botMessageContent")
        messageLb.setFont(QFont("Segoe UI", 11))
        messageLb.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        messageLb.setWordWrap(True)
        if isUserMessage:
            messageLb.setStyleSheet("background: #0AB6D1; color: white; padding: 10px; border-radius: 8px;")
            messageLayout.addStretch()
            messageLayout.insertWidget(1, messageLb, 0, Qt.AlignmentFlag.AlignRight)
        else:
            messageLb.setStyleSheet("background: #E0E0E0 ; color: black; padding: 10px; border-radius: 8px;")
            messageLayout.insertWidget(0, messageLb, 0, Qt.AlignmentFlag.AlignLeft)
            messageLayout.addStretch()

        self.chatLayout.addWidget(messageWidget)
        return messageWidget

    def clearMessages(self):
        layout = self.widget().layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
    def resizeEvent(self, arg__1):
        super().resizeEvent(arg__1)
        self.widget().adjustSize()
        self.widget().setFixedWidth(self.viewport().width())
        for item in self.widget().findChildren(QLabel, "messageContent"):
            item.setMaximumWidth(self.widget().width() * 0.4)
        