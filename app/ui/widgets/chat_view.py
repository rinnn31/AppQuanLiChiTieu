from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont

class ChatView(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        chatContainer = QWidget()
        chatContainer.setStyleSheet("background: white; margin: 0px;")
        chatLayout = QVBoxLayout(chatContainer)
        chatLayout.setContentsMargins(10,10,10,10)
        chatLayout.setSpacing(10)
        self.setWidget(chatContainer)
        self.setWidgetResizable(True)

    def pushMessage(self, message : str, isUserMessage : bool):
        messageWidget = QWidget()
        messageWidget.setObjectName("messageWidget")
        messageWidget.setStyleSheet("background: red;")
        messageWidget.setMax
        messageWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        messageLayout = QHBoxLayout(messageWidget)

        messageLb = QLabel(message)
        messageLb.setFont(QFont("Segoe UI", 11))
        messageLb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        messageLb.setWordWrap(True)
        if isUserMessage:
            messageLb.setStyleSheet("background: #0AB6D1; color: white; padding: 10px; border-radius: 8px;")
            messageLayout.addStretch()
            messageLayout.addWidget(messageLb)
        else:
            messageLb.setStyleSheet("background: #E0E0E0 ; color: black; padding: 10px; border-radius: 8px;")
            messageLayout.addWidget(messageLb)
            messageLayout.addStretch()

        self.widget().layout().addWidget(messageWidget)

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
        for item in self.widget().findChildren(QWidget, "messageWidget"):
            item.setMaximumWidth(self.widget().width() * 0.5)
        