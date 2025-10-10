import google.generativeai as genai
from PySide6.QtCore import QObject, Signal, QThread
from core.transaction_manager import TransactionManager
from datetime import datetime

class BotAssistant:
    API_KEY = "AIzaSyAP2lAU--C_QZzxcE48MH_k37xiWLHmHAM"

    ASSISTANT_SYSTEM_PROMPT = """
    Bạn là một trợ lý ảo giúp người dùng quản lý chi tiêu cá nhân. Bạn phải tuân thủ các quy tắc sau:
    1. Bạn chỉ trả lời các câu hỏi liên quan đến quản lý chi tiêu cá nhân, lập kế hoạch tài chính, mẹo tiết kiệm tiền, phân tích thói quen chi tiêu và cách sử dụng ứng dụng ChiTiêu+. Nếu câu hỏi không liên quan, bạn lịch sự từ chối trả lời.
    2. Bạn không bao giờ hỏi người dùng về thông tin cá nhân như tên, địa chỉ
    3. Mỗi khi người dùng yêu cầu phân tích từ thống kê chi tiêu của người dùng, hãy phản hồi chính xác câu truy vấn có định dạng như dưới đây, sau đó chờ dữ liệu từ ứng dụng ChiTiêu+ để trả lời câu hỏi của người dùng, vui lòng không thêm bất kỳ thông tin nào khác ngoài câu truy vấn. Các câu truy vấn có thể là:
        - GET_TOTAL_FINANCE:<start_date>:<end_date> # Ví dụ GET_TOTAL_FINANCE:2023-01-01:2023-12-31
        - GET_TRANSACTIONS:<start_date>:<end_date> # Ví dụ GET_ALL_TRANSACTIONS:2023-01-01:2023-12-31
    4. Bổ sung cho quy tắc 3, bạn có thể trả về nhiều câu truy vấn liên tiếp nếu cần thêm dữ liệu để trả lời câu hỏi của người dùng. Mỗi câu truy vấn phải được đặt trên một dòng riêng biệt. Nếu không thể phân tích câu hỏi của người dùng thành các câu truy vấn, hãy trả lời người dùng rằng bạn không thể trả lời câu hỏi của họ. Nếu câu hỏi của người dùng không yêu cầu phân tích từ dữ liệu, hãy trả lời trực tiếp câu hỏi của họ.
    """


    def __init__(self, api_key: str = None):
        genai.configure(api_key=api_key if api_key else BotAssistant.API_KEY)
        self._model = genai.GenerativeModel(system_instruction=BotAssistant.ASSISTANT_SYSTEM_PROMPT,
                                            model_name="gemini-2.5-flash")
        
        self._chat = self._model.start_chat()

    def setTransactionManager(self, transactionManager : TransactionManager):
        self.transactionManager = transactionManager

    def clearMessages(self):
        self._chat = self._model.start_chat(history=[])

    def _handleFinanceQueryIfNeeded(self, response: str):
        lines = response.split("\n")
        secondStageMessages = []
        for line in lines:
            line = line.strip()

            if line.startswith("GET_TOTAL_FINANCE:"):
                parts = line.split(":")
                if len(parts) == 3:
                    start_date, end_date = datetime.strptime(parts[1], "%Y-%m-%d"),datetime.strptime(parts[2], "%Y-%m-%d")
                    res = self.transactionManager.getDailyTotalsInPeriod(startDate=start_date, endDate=end_date)
                    total_income, total_expense = 0, 0
                    for val in res.values() :
                        total_income += val[0]
                        total_expense += val[1]
                    secondStageMessages.append(f"- Tổng thu nhập từ {start_date} đến {end_date} là {total_income} VND. Tổng chi tiêu là {total_expense} VND.")
                else:
                    secondStageMessages.append("- Câu truy vấn GET_TOTAL_FINANCE không hợp lệ.")
            
            elif line.startswith("GET_ALL_TRANSACTIONS:"):
                parts = line.split(":")
                if len(parts) == 3:
                    start_date, end_date = datetime.strptime(parts[1], "%Y-%m-%d"),datetime.strptime(parts[2], "%Y-%m-%d")
                    transactions = self.transactionManager.getTransactions(startDate=start_date, endDate=end_date)
                    if transactions:
                        secondStageMessages.append(f"- Danh sách giao dịch từ {start_date} đến {end_date}:")
                        for t in transactions:
                            t_type = "Thu nhập" if t.type == 0 else "Chi tiêu"
                            secondStageMessages.append(f"- {t.date}: {t_type} - {t.category} - {t.amount} VND - {t.note}")
                    else:
                        secondStageMessages.append(f"- Không có giao dịch nào từ {start_date} đến {end_date}.")
                else:
                    secondStageMessages.append("- Câu truy vấn GET_ALL_TRANSACTIONS không hợp lệ.")
        
        if secondStageMessages:
            self._chat.send_message("\n".join(secondStageMessages))
    
    def sendMessage(self, message: str):
        self._chat.send_message(message)
        self._handleFinanceQueryIfNeeded(self._chat.last.text)
        return self._chat.last.text
    
    
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
    stateChanged = Signal(str)
    messageReceived = Signal(str)

    def __init__(self, parent=None, botAssistant: BotAssistant = None):
        super().__init__(parent)
        self._botAssistant = botAssistant if botAssistant else BotAssistant()
        self._currentThread = None
    
    def sendMessage(self, message: str, force: bool = False):
        if force:
            self.stopCurrentChatting()
        if self._currentThread is not None and self._currentThread.isRunning():
            return
        
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
    
