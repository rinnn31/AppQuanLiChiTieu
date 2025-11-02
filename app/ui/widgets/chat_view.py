from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QFont, QMovie, QFontMetrics, QPainter

class ChatItem(QWidget):
    def __init__(self, parent=None, isOutgoingMessage: bool = True, message: str = "", isTypingType = False):
        super().__init__(parent)
        self._isTypingType = isTypingType
        self._message = message
        self._isOutgoingMessage = isOutgoingMessage
        self.setupUi()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Tính lại kích thước tin nhắn khi thay đổi kích thước khung chat
        self._calculateMessageSize()

    def _calculateMessageSize(self):
        # Nếu là tin nhắn biểu tượng đang gõ thì không cần tính kích thước
        if self._isTypingType:
            return
        
        #Tính kích thước tin nhắn, nếu vượt quá 45% chiều rộng của khung chat thì cho xuống dòng
        metrics = QFontMetrics(self._messageLb.font())
        messageRect = metrics.boundingRect(QRect(0,0,10000, 10000), 0, self._message)
        if messageRect.width() > self.width() * 0.45:
            self._messageLb.setWordWrap(True)
            self._messageLb.setFixedWidth(self.width() * 0.45)
        else:
            self._messageLb.setWordWrap(False)
            self._messageLb.setFixedWidth(messageRect.width() + 30)
        self._messageLb.adjustSize()

    def setupUi(self):
        layout = QHBoxLayout(self)
        self._messageLb = QLabel(self)
        self._messageLb.setText(self._message)
        self._messageLb.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self._messageLb.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        self._messageLb.setWordWrap(True)
        self._messageLb.setFont(QFont("Segoe UI", 11))
        
        # Thiết lập giao diện cho tin nhắn đang gõ
        if self._isTypingType:
            self._messageLb.setScaledContents(True)
            self._messageLb.setFixedSize(65, 40)
            self._movie = QMovie(":resources/gifs/typing.gif")
            self._movie.setSpeed(150)
            self._movie.setScaledSize(QSize(50, 40))
            self._messageLb.setMovie(self._movie)
            self._movie.start()
        
        # Thiết lập giao diện cho tin nhắn gửi và nhận
        if self._isOutgoingMessage:
            self._messageLb.setStyleSheet("background: #0AB6D1; color: white; padding: 10px; border-radius: 8px;")
            layout.addStretch(1)
            layout.addWidget(self._messageLb, 0, Qt.AlignmentFlag.AlignRight)
        else:
            self._messageLb.setStyleSheet("background: #E0E0E0 ; color: black; padding: 10px; border-radius: 8px;")
            layout.addWidget(self._messageLb, 0, Qt.AlignmentFlag.AlignLeft)
            layout.addStretch(1)          
        self.setLayout(layout)
        self._calculateMessageSize()


    def isTypingType(self) -> bool:
        return self._isTypingType
    
    def isOutgoingMessage(self) -> bool:
        return self._isOutgoingMessage

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
                width: 6px;
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
        # Tự động cuộn xuống dưới khi có tin nhắn mới
        self.verticalScrollBar().rangeChanged.connect(lambda: self.verticalScrollBar().setValue(self.verticalScrollBar().maximum()))

    def pushMessage(self, message: str, isOutgoingMessage: bool = True):
        # Nếu là tin nhắn từ trợ lý ảo thì tắt trạng thái đang gõ
        if not isOutgoingMessage:
            self.disableIncomeChattingState()

        # Tạo bong bóng chat mới và thêm vào giao diện
        messageItem = ChatItem(self._chatContainer, isOutgoingMessage=isOutgoingMessage, message=message)
        self._chatLayout.addWidget(messageItem)
    
    
    def enableIncomeChattingState(self):
        '''
        Hiện thị trạng thái đang gõ của trợ lý ảo
        '''
        # Nếu đã có trạng thái đang gõ thì không thêm nữa
        if self._getTypingStateItem() is not None:
            return
        messageItem = ChatItem(self._chatContainer, isOutgoingMessage=False, isTypingType=True)
        self._chatLayout.addWidget(messageItem)
        

    def disableIncomeChattingState(self):
        '''
        Ẩn trạng thái đang gõ của trợ lý ảo
        '''

        typingStateItem = self._getTypingStateItem()
        if typingStateItem is not None:
            typingStateItem.setParent(None)
            typingStateItem.deleteLater()

    def _getTypingStateItem(self) -> ChatItem | None:
        for layoutIndex in range(self._chatLayout.count()-1, -1, -1):
            item = self._chatLayout.itemAt(layoutIndex).widget()
            if isinstance(item, ChatItem) and not item.isOutgoingMessage() and item.isTypingType():
                return item
        return None

    def clearMessages(self):
        '''
        Xóa toàn bộ tin nhắn trong giao diện chat
        '''
        layout = self.widget().layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        