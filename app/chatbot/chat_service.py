from PySide6.QtCore import QObject, QThread, Signal
from app.chatbot.bot_assistant import BotAssistant

class ChattingThread(QThread):
    '''
    Thread để gửi và nhận tin nhắn từ BotAssistant mà không làm đơ giao diện người dùng.
    '''
    responseReceived = Signal(str)

    def __init__(self, botAssistant: BotAssistant, message: str, parent=None):
        super().__init__(parent)
        self._botAssistant = botAssistant
        self._message = message

    def run(self):
        try:
            resp =  self._botAssistant.sendMessage(self._message)
            self.responseReceived.emit(resp)
        except Exception as e:
            print(f"Error in ChattingThread: {e}")
            self.responseReceived.emit("Xin lỗi, đã có lỗi xảy ra khi xử lý yêu cầu của bạn.")

class ChattingService(QObject):
    '''
    Dịch vụ trò chuyện với BotAssistant trong một thread riêng biệt.
    '''
    stateChanged = Signal(str)
    messageReceived = Signal(str)

    def __init__(self, parent=None, botAssistant: BotAssistant = None):
        super().__init__(parent)
        self._botAssistant = botAssistant if botAssistant else BotAssistant()
        self._currentThread = None
    
    def sendMessage(self, message: str, force: bool = False):
        # Nếu force là True, dừng cuộc trò chuyện hiện tại và bắt đầu cuộc trò chuyện mới, ngược lại nếu đang có cuộc trò chuyện thì bỏ qua yêu cầu mới
        if force:
            self.stopCurrentChatting()
        if self._currentThread is not None and self._currentThread.isRunning():
            return
        
        # Khởi tạo, gửi và chờ nhận phản hồi trong một thread riêng biệt
        self._currentThread = ChattingThread(self._botAssistant, message)
        self._currentThread.responseReceived.connect(self.onResponseReceived)
        self._currentThread.start()

        self.stateChanged.emit("busy")

    def stopCurrentChatting(self):
        if self._currentThread is not None and self._currentThread.isRunning():
            self._currentThread.terminate()
            self._currentThread.wait()
            self.stateChanged.emit("idle")
            self._currentThread = None

    def onResponseReceived(self, response: str):
        self.messageReceived.emit(response)
        self.stateChanged.emit("idle")
        self._currentThread = None
