from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QColor, QFont
import datetime
from app.ui.overview_ui import Ui_OverviewPage
from app.utils.window_helper import applyDropShadow

class OverviewPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.transactionManager = QApplication.instance().getTransactionManager()

        self.ui = Ui_OverviewPage()
        self.ui.setupUi(self)
        
        applyDropShadow(self.ui.monthlySummariesCard, radius=5)
        applyDropShadow(self.ui.recentTransactionCard, radius=5)
        applyDropShadow(self.ui.comparisionCard, radius=5)

        fnt = QFont("Segoe UI", 14, QFont.Weight.Bold)
        self.ui.incomePieChart.setTitle("Thu nhập", fnt, QColor("#27AE60"))
        self.ui.expensePieChart.setTitle("Chi tiêu", fnt, QColor("#EB5757"))

    def refreshData(self):
        # Hàm được gọi mỗi khi trang được hiển thị để làm mới dữ liệu
        self.refreshMonthlySummaryData()
        self.refreshComparisionData()
        self.refreshTransactionData()
        
    def cleanData(self):
        # Hàm được gọi mỗi khi trang bị ẩn đi để dọn dẹp dữ liệu hiển thị
        self.ui.incomePieChart.clearData()
        self.ui.expensePieChart.clearData()
        self.ui.cmpChart.clearData()
        self.ui.allTransTab.clearTransactions()
        self.ui.incomeTransTab.clearTransactions()
        self.ui.expenseTransTab.clearTransactions()

    def refreshMonthlySummaryData(self):
        # Lấy dữ liệu tóm tắt tháng hiện tại
        curMonth = datetime.datetime.now().strftime("%Y-%m")
        curSummary = self.transactionManager.getMonthlySummary(curMonth)
        
        # Lấy chi tiết tổng số tiền thu/chi theo danh mục
        incomeCategories = self.transactionManager.getMonthlyCategoriesAmounts(curMonth, 0)
        # Tổng chi của từng danh mục dict[str,int]
        expenseCategories = self.transactionManager.getMonthlyCategoriesAmounts(curMonth, 1)

        from app.utils.value_formatter import getShortMoneyString
        fnt = QFont("Segoe UI", 14, QFont.Weight.Bold)
        # Cập nhật dữ liệu số tiền thu theo danh mục lên biểu đồ hình tròn
        self.ui.incomePieChart.setData(incomeCategories)
        # Cập nhật số tiền tổng lên giữa biểu đồ với định dạng rút gọn
        self.ui.incomePieChart.setCenterText(getShortMoneyString(curSummary.total_income), fnt, QColor("#27AE60"))
        
        # Cập nhật dữ liệu số tiền chi theo danh mục lên biểu đồ hình tròn
        self.ui.expensePieChart.setData(expenseCategories)
        # Cập nhật số tiền tổng lên giữa biểu đồ với định dạng rút gọn
        self.ui.expensePieChart.setCenterText(getShortMoneyString(curSummary.total_expense), fnt, QColor("#EB5757"))
        

    def refreshComparisionData(self):
        curDate = datetime.datetime.now() # Lấy ngày hiện tại
        lastDate = curDate - datetime.timedelta(days=29) # Lùi về 29 ngày

        # Lấy dữ liệu tổng thu/chi hàng ngày trong 30 ngày gần nhất
        datas = self.transactionManager.getDailyTotalsInPeriod(lastDate, curDate)
        # Tạo bộ dữ liệu cho biểu đường
        values = ()
        xAxisValues = []
        for i in range(30):
            day = (lastDate + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            # Kiểm tra xem có dữ liệu cho ngày này không, nếu không có thì gán giá trị 0
            if day not in datas:
                values += (day, 0, 0),
            else:
                income, expense = datas[day]
                values += (day, income, expense),

        
        # Tạo danh sách nhãn trục x (mỗi 5 ngày một nhãn)
        for i in range(0, 30, 5):
            day = lastDate + datetime.timedelta(days=i)
            xAxisValues.append(day.strftime("%d/%m"))
        xAxisValues.append(curDate.strftime("%d/%m"))

        # Cập nhật dữ liệu lên biểu đồ so sánh
        self.ui.cmpChart.setData(values, xAxisValues, "Ngày")        
    
    def refreshTransactionData(self):
        # Lấy danh sách 30 giao dịch gần nhất
        transactions = self.transactionManager.getTransactions(limit=30)
        # Cập nhật dữ liệu lên các tab giao dịch gồm tất cả, thu nhập và chi tiêu
        self.ui.allTransTab.loadTransactions(transactions)
        self.ui.incomeTransTab.loadTransactions([t for t in transactions if t.type == 0])
        self.ui.expenseTransTab.loadTransactions([t for t in transactions if t.type == 1])

    def hideEvent(self, event):
        super().hideEvent(event)
        self.cleanData()
        
    