from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QMovie

class ChatItem(QWidget):
    def __init__(self, parent=None, isOutgoingMessage: bool = True, message: str = "", isTypingType = False):
        super().__init__(parent)
        self._isTypingType = isTypingType
        self._message = message
        self._isOutgoingMessage = isOutgoingMessage
        self.setupUi()

    def messageClicked(self, event):
        print("Message clicked")
        print("Current max width: " + self._messageLb.maximumWidth().__str__())
        print("Current size: " + self._messageLb.size().__str__())
        print("Current size hint: " + self._messageLb.sizeHint().__str__())
        print("Current self size: " + self.size().__str__())


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._messageLb.setMaximumWidth(int(self.width() * 0.45))

    def setupUi(self):
        layout = QHBoxLayout(self)
        self._messageLb = QLabel(self)
        self._messageLb.setText(self._message)
        self._messageLb.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self._messageLb.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        self._messageLb.setFont(QFont("Segoe UI", 11))
        self._messageLb.setWordWrap(True)
        if self._isTypingType:
            self._messageLb.setScaledContents(True)
            self._messageLb.setFixedSize(65, 40)
            self._movie = QMovie(":resources/gifs/typing.gif")
            self._movie.setSpeed(150)
            self._movie.setScaledSize(QSize(50, 30))
            self._messageLb.setMovie(self._movie)
            self._movie.start()
        if self._isOutgoingMessage:
            print("outgoing")
            self._messageLb.setStyleSheet("background: #0AB6D1; color: white; padding: 10px; border-radius: 8px;")
            layout.addStretch(1)
            layout.addWidget(self._messageLb, 0, Qt.AlignmentFlag.AlignRight)
        else:
            self._messageLb.setStyleSheet("background: #E0E0E0 ; color: black; padding: 10px; border-radius: 8px;")
            layout.addWidget(self._messageLb, 0, Qt.AlignmentFlag.AlignLeft)
            layout.addStretch(1)          
        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setFixedHeight(self._messageLb.sizeHint().height() + 20)

    def isTypingType(self) -> bool:
        return self._isTypingType
    
    def isOutgoingMessage(self) -> bool:
        return self._isOutgoingMessage
    
    def setMaxContentWidth(self, width: int):
        print("Set max width: " + width.__str__())
        self._messageLb.setMaximumWidth(width)

    def __del__(self):
        if hasattr(self, "_movie"):
            self._movie.stop()
            self._movie.deleteLater()

class ChatView(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setStyleSheet("""
            QWidget {
                background: white;
                border: none;
            }
                           
            QScrollBar
            {
                background-color: rgb(180, 180, 180);
                border:1px transparent;
                border-radius:3px;
            }
            QScrollBar::handle
            {
                background-color: rgb(122, 122, 122);
                border-radius:3px;
            }
            QScrollBar::sub-page
            {
                background: none;
                width: 0px;
                height: 0px;
            }
            QScrollBar::add-page
            {
                background: none;
                width: 0px;
                height: 0px;
            }

            QScrollBar::sub-line
            {
                background: none;
                width: 0px;
                height: 0px;
            }
                           
            QScrollBar::add-line
            {
                background: none;
                width: 0px;
                height: 0px;
            }

            QScrollBar:vertical {
                witdh: 6px;
            }

            QScrollBar:horizontal {
                height: 6px
            }""")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self._chatContainer = QWidget()
        self._chatContainer.setStyleSheet("margin: 0px;")
        self._chatLayout = QVBoxLayout(self._chatContainer)
        self._chatLayout.setContentsMargins(30,50,30,30)
        self._chatLayout.setSpacing(0)
        self._chatLayout.setAlignment(Qt.AlignTop)
        self.setWidget(self._chatContainer)
        self.setWidgetResizable(True)
        self.verticalScrollBar().setMaximumWidth(6)

    def pushMessage(self, message: str, isOutgoingMessage: bool = True):
        if not isOutgoingMessage:
            self.disableIncomeChattingState()
        messageItem = ChatItem(self._chatContainer, isOutgoingMessage=isOutgoingMessage, message=message)
        self._chatLayout.addWidget(messageItem)
    
    def enableIncomeChattingState(self):
        if self.getTypingStateItem() is not None:
            return
        messageItem = ChatItem(self._chatContainer, isOutgoingMessage=False, isTypingType=True)
        self._chatLayout.addWidget(messageItem)

    def disableIncomeChattingState(self):
        typingStateItem = self.getTypingStateItem()
        if typingStateItem is not None:
            typingStateItem.setParent(None)
            typingStateItem.deleteLater()

    def getTypingStateItem(self) -> ChatItem | None:
        for layoutIndex in range(self._chatLayout.count()-1, -1, -1):
            item = self._chatLayout.itemAt(layoutIndex).widget()
            if isinstance(item, ChatItem) and not item.isOutgoingMessage() and item.isTypingType():
                return item
        return None

    def clearMessages(self):
        layout = self.widget().layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        