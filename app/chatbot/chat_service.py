from PySide6.QtCore import QObject, QThread, Signal
from app.chatbot.bot_assistant import BotAssistant

class ChattingThread(QThread):
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
    # Tín hiệu phát ra khi trạng thái của dịch vụ thay đổi (ví dụ: từ idle sang busy)
    stateChanged = Signal(str)
    # Tín hiệu phát ra khi nhận được tin nhắn phản hồi từ bot trợ lý ảo
    messageReceived = Signal(str)

    def __init__(self, botAssistant, parent=None):
        super().__init__(parent)
        self._botAssistant = botAssistant
        # Biến để theo dõi thread hiện tại
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

        # Cập nhật trạng thái về busy
        self.stateChanged.emit("busy")

    def stopCurrentChatting(self):
        # Kiểm tra xem có thread nào đang chạy không
        if self._currentThread is not None and self._currentThread.isRunning():
            # Dừng thread hiện tại
            self._currentThread.terminate()
            self._currentThread.wait()
            # Thông báo trạng thái về idle
            self.stateChanged.emit("idle")
            self._currentThread = None

    def onResponseReceived(self, response: str):
        # Phát tín hiệu phản hồi đã nhận được
        self.messageReceived.emit(response)
        # Cập nhật trạng thái về idle
        self.stateChanged.emit("idle")
        self._currentThread = None
