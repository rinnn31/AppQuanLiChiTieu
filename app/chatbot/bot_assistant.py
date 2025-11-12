import google.generativeai as genai
from datetime import datetime
from app.database.transaction_manager import TransactionManager
from app.utils.transaction_style import INCOME_CATEGORIES , EXPENSE_CATEGORIES

class BotAssistant:
    API_KEY = None

    ASSISTANT_SYSTEM_PROMPT = f"""
    Bạn là một trợ lý ảo giúp người dùng quản lý chi tiêu cá nhân. Bạn phải tuân thủ các quy tắc sau:
    1. Bạn chỉ trả lời các câu hỏi liên quan đến quản lý chi tiêu cá nhân, lập kế hoạch tài chính, mẹo tiết kiệm tiền, phân tích thói quen chi tiêu và cách sử dụng ứng dụng ChiTiêu+. Nếu câu hỏi không liên quan, bạn lịch sự từ chối trả lời.
    2. Mỗi khi người dùng yêu cầu phân tích từ thống kê chi tiêu của người dùng, hãy phản hồi chính xác câu truy vấn có định dạng như dưới đây, sau đó chờ dữ liệu từ ứng dụng ChiTiêu+ để trả lời câu hỏi của người dùng, vui lòng không thêm bất kỳ thông tin nào khác ngoài câu truy vấn. Các câu truy vấn có thể là:
        - GET_TOTAL_FINANCE:<start_date>:<end_date> # Ví dụ GET_TOTAL_FINANCE:2023-01-01:2023-12-31
        - GET_TRANSACTIONS:<start_date>:<end_date> # Ví dụ GET_TRANSACTIONS:2023-01-01:2023-12-31
        - GET_CATEGORY_FINANCE:<start_date>:<end_date>:<category> # Danh sách những danh mục hợp lệ {",".join(INCOME_CATEGORIES)},{",".join(EXPENSE_CATEGORIES)}
    3. Bổ sung cho quy tắc 3, bạn có thể trả về nhiều câu truy vấn liên tiếp nếu cần thêm dữ liệu để trả lời câu hỏi của người dùng. Mỗi câu truy vấn phải được đặt trên một dòng riêng biệt. Nếu không thể phân tích câu hỏi của người dùng thành các câu truy vấn, hãy trả lời người dùng rằng bạn không thể trả lời câu hỏi của họ. Nếu câu hỏi của người dùng không yêu cầu phân tích từ dữ liệu, hãy trả lời trực tiếp câu hỏi của họ.
    4. Tháng này là tháng {datetime.now().month} năm {datetime.now().year}.
    """


    def __init__(self):
        # Khởi tạo mô hình Gemini sử dụng model 2.0-flash với khoá API và hệ thống prompt
        genai.configure(api_key=BotAssistant.API_KEY)
        self._model = genai.GenerativeModel(system_instruction=BotAssistant.ASSISTANT_SYSTEM_PROMPT,
                                            model_name="gemini-2.0-flash")
        self._chat = self._model.start_chat()

    def setApiKey(cls, api_key: str):
        cls.API_KEY = api_key

    def setTransactionManager(self, transactionManager : TransactionManager):
        self._transactionManager = transactionManager

    def clearMessages(self):
        self._chat = self._model.start_chat(history=[])

    def _handleFinanceQueryIfNeeded(self, response: str):
        lines = response.split("\n")
        # Lưu trữ các dự liệu đã truy vấn
        secondStageMessages = []
        for line in lines:
            line = line.strip()
            # Kiểm tra xem có phải định dạng câu truy vấn không
            if line.startswith("GET_TOTAL_FINANCE:"):
                tokens = line.split(":")
                if len(tokens) == 3:
                    start_date, end_date = datetime.strptime(tokens[1], "%Y-%m-%d"),datetime.strptime(tokens[2], "%Y-%m-%d")
                    res = self._transactionManager.getDailyTotalsInPeriod(startDate=start_date, endDate=end_date)
                    total_income, total_expense = 0, 0
                    for val in res.values() :
                        total_income += val[0]
                        total_expense += val[1]
                    secondStageMessages.append(f"- Tổng thu nhập từ {start_date} đến {end_date} là {total_income} VND. Tổng chi là {total_expense} VND.")
                else:
                    secondStageMessages.append("- Câu truy vấn GET_TOTAL_FINANCE không hợp lệ.")      
            elif line.startswith("GET_TRANSACTIONS:"):
                tokens = line.split(":")
                if len(tokens) == 3:
                    start_date, end_date = datetime.strptime(tokens[1], "%Y-%m-%d"),datetime.strptime(tokens[2], "%Y-%m-%d")
                    transactions = self._transactionManager.getTransactions(startDate=start_date, endDate=end_date)
                    if transactions:
                        secondStageMessages.append(f"- Danh sách giao dịch từ {start_date} đến {end_date}:")
                        for t in transactions:
                            t_type = "Thu nhập" if t.type == 0 else "Chi tiêu"
                            secondStageMessages.append(f"- {t.date}: {t_type} - {t.category} - {t.amount} VND - {t.note}")
                    else:
                        secondStageMessages.append(f"- Không có giao dịch nào từ {start_date} đến {end_date}.")
                else:
                    secondStageMessages.append("- Câu truy vấn GET_ALL_TRANSACTIONS không hợp lệ.")
            elif line.startswith("GET_CATEGORY_FINANCE:"):
                tokens = line.split(":")
                if len(tokens) == 4:
                    start_date, end_date = datetime.strptime(tokens[1], "%Y-%m-%d"),datetime.strptime(tokens[2], "%Y-%m-%d")
                    transactions = self._transactionManager.getTransactions(startDate=start_date, endDate=end_date)
                    if transactions:
                        secondStageMessages.append(f"- Danh sách giao dịch thuoc danh muc {tokens[3]} từ {start_date} đến {end_date}:")
                        check = False
                        for t in transactions:
                           if t.category == tokens[3]:
                               secondStageMessages.append(f"-{t.date}: {t.amount}")
                               check=True
                        if not check:
                            secondStageMessages.append(f"- Khong co giao dịch nao thuoc danh muc {tokens[3]} từ {start_date} đến {end_date}:")
                    else:
                        secondStageMessages.append(f"- Không có giao dịch nào từ {start_date} đến {end_date}.")
                else:
                    secondStageMessages.append("- Câu truy vấn GET_CATEGORY_FINANCE không hợp lệ.")
        
        # Nếu có dữ liệu, gửi chúng đến bot trợ lý ảo để nhận phản hồi thứ hai
        if secondStageMessages:
            self._chat.send_message("\n".join(secondStageMessages))
    
    def sendMessage(self, message: str):
        # Gửi tin nhắn từ người dùng đến bot trợ lý ảo
        self._chat.send_message(message)
        # Kiêm tra và xử lý các câu truy vấn tài chính nếu cần
        self._handleFinanceQueryIfNeeded(self._chat.last.text)
        # Đưa ra phản hồi cuối cùng từ bot trợ lý ảo
        return self._chat.last.text
    
