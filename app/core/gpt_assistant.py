import google.generativeai as genai
from core.transaction_manager import TransactionManager

API_KEY = "AIzaSyAP2lAU--C_QZzxcE48MH_k37xiWLHmHAM"

GPT_ASSISTANT_SYSTEM_PROMPT = """
Bạn là một trợ lý ảo giúp người dùng quản lý chi tiêu cá nhân. Bạn phải tuân thủ các quy tắc sau:
1. Bạn chỉ trả lời các câu hỏi liên quan đến quản lý chi tiêu cá nhân, lập kế hoạch tài chính, mẹo tiết kiệm tiền, phân tích thói quen chi tiêu và cách sử dụng ứng dụng ChiTiêu+. Nếu câu hỏi không liên quan, bạn lịch sự từ chối trả lời.
2. Bạn không bao giờ hỏi người dùng về thông tin cá nhân như tên, địa chỉ
3. Mỗi khi người dùng yêu cầu phân tích từ thống kê chi tiêu của người dùng, hãy phản hồi chính xác câu truy vấn có định dạng như dưới đây, sau đó chờ dữ liệu từ ứng dụng ChiTiêu+ để trả lời câu hỏi của người dùng, vui lòng không thêm bất kỳ thông tin nào khác ngoài câu truy vấn. Các câu truy vấn có thể là:
    - GET_TOTAL_FINANCE:<start_date>:<end_date> # Ví dụ GET_TOTAL_FINANCE:2023-01-01:2023-12-31
    - GET_ALL_TRANSACTIONS:<start_date>:<end_date> # Ví dụ GET_ALL_TRANSACTIONS:2023-01-01:2023-12-31
    - GET_CATEGORY_SUMMARY:<start_date>:<end_date>:<category>:<type> # Ví dụ GET_CATEGORY_SUMMARY:2023-01-01:2023-12-31:Food:1
4. Bổ sung cho quy tắc 3, bạn có thể trả về nhiều câu truy vấn liên tiếp nếu cần thêm dữ liệu để trả lời câu hỏi của người dùng. Mỗi câu truy vấn phải được đặt trên một dòng riêng biệt. Nếu không thể phân tích câu hỏi của người dùng thành các câu truy vấn, hãy trả lời người dùng rằng bạn không thể trả lời câu hỏi của họ. Nếu câu hỏi của người dùng không yêu cầu phân tích từ dữ liệu, hãy trả lời trực tiếp câu hỏi của họ.
"""

class GptAssistant:
    def __init__(self, api_key: str = None):
        genai.configure(api_key=api_key if api_key else API_KEY)
        self._model = genai.GenerativeModel(system_instruction=GPT_ASSISTANT_SYSTEM_PROMPT, model_name="gemini-2.5-flash")
        self._chat = self._model.start_chat()

    def addTransactionManager(self, transactionManager : TransactionManager):
        self.transactionManager = transactionManager

    def clearMessages(self):
        self._chat = self._model.start_chat(history=[])

    def _handleRawResponse(self, response: str) -> str:
        lines = response.split("\n")
        results = []
        for line in lines:
            line = line.strip()
            if line.startswith("GET_TOTAL_FINANCE:"):
                parts = line.split(":")
                if len(parts) == 3:
                    start_date, end_date = parts[1], parts[2]
                    total_income, total_expense = self.transactionManager.getTotalFinance(start_date, end_date)
                    results.append(f"Tổng thu nhập từ {start_date} đến {end_date} là {total_income} VND. Tổng chi tiêu là {total_expense} VND.")
                else:
                    results.append("Câu truy vấn GET_TOTAL_FINANCE không hợp lệ.")
            elif line.startswith("GET_ALL_TRANSACTIONS:"):
                parts = line.split(":")
                if len(parts) == 3:
                    start_date, end_date = parts[1], parts[2]
                    transactions = self.transactionManager.getTransactions(startDate=start_date, endDate=end_date)
                    if transactions:
                        results.append(f"Danh sách giao dịch từ {start_date} đến {end_date}:")
                        for t in transactions:
                            t_type = "Thu nhập" if t.type == 0 else "Chi tiêu"
                            results.append(f"- {t.date}: {t_type} - {t.category} - {t.amount} VND - {t.note}")
                    else:
                        results.append(f"Không có giao dịch nào từ {start_date} đến {end_date}.")
                else:
                    results.append("Câu truy vấn GET_ALL_TRANSACTIONS không hợp lệ.")
            elif line.startswith("GET_CATEGORY_SUMMARY:"):
                parts = line.split(":")
                if len(parts) == 5:
                    start_date, end_date, category, t_type = parts[1], parts[2], parts[3], int(parts[4])
                    total_amount = self.transactionManager.getCategorySummary(start_date, end_date, category, t_type)
                    t_type_str = "thu nhập" if t_type == 0 else "chi tiêu"
                    results.append(f"Tổng {t_type_str} trong mục '{category}' từ {start_date} đến {end_date} là {total_amount} VND.")
                else:
                    results.append("Câu truy vấn GET_CATEGORY_SUMMARY không hợp lệ.")
            else:
                results.append(line)
        return "\n".join(results)
    
    def sendMessage(self, message: str):
        self._chat.send_message(message)
        return self._chat.last.text
    
        

