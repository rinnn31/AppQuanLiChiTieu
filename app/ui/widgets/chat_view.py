from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class ChatView(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        chatContainer = QWidget()
        chatLayout = QVBoxLayout(chatContainer)
        chatLayout.setContentsMargins(10,10,10,10)
        chatLayout.setSpacing(10)
        
        self.setWidget(chatContainer)

    def pushMessage(self, message : str, isUserMessage : bool):
        messageLb = QLabel(message)
        messageLb.setWordWrap(True)
        if isUserMessage:
            messageLb.setStyleSheet("background: #0AB6D1; color: white; padding: 10px; border-radius: 8px;")
            messageLb.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            messageLb.setStyleSheet("background: #E0E0E0; color: black; padding: 10px; border-radius: 8px;")
            messageLb.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.widget().layout().addWidget(messageLb)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def clearMessages(self):
        layout = self.widget().layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
    def resizeEvent(self, arg__1):
        super().resizeEvent(arg__1)
        self.widget().setFixedWidth(self.viewport().width())
