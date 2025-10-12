from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QColor, QFont
import datetime
from dateutil.relativedelta import relativedelta
from ui.overview_ui import Ui_OverviewPage
from utils.window_helper import applyDropShadow
from core.transaction import MonthlySummary

class OverviewPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.transactionManager = QApplication.instance().getTransactionManager()

        self.ui = Ui_OverviewPage()
        self.ui.setupUi(self)
        applyDropShadow(self.ui.monthlySummariesCard, radius=5)
        applyDropShadow(self.ui.recentTransactionCard, radius=5)
        applyDropShadow(self.ui.comparisionCard, radius=5)


    def refreshData(self):
        self.refreshMonthlySummaryData()
        self.refreshComparisionData()
        self.refreshTransactionData()
        
    def cleanData(self):
        self.ui.incomePieChart.clearData()
        self.ui.expensePieChart.clearData()
        self.ui.cmpChart.clearData()
        self.ui.allTransTab.clearTransactions()
        self.ui.incomeTransTab.clearTransactions()
        self.ui.expenseTransTab.clearTransactions()

    def refreshMonthlySummaryData(self):
        curMonth = datetime.datetime.now().strftime("%Y-%m")
        prevMonth = (datetime.datetime.now() - relativedelta(months=1)).strftime("%Y-%m")

        curSummary = self.transactionManager.getMonthlySummary(curMonth)
        prevSummary = self.transactionManager.getMonthlySummary(prevMonth)
        if curSummary is None:
            curSummary = MonthlySummary(curMonth, 0, 0, 0)
        if prevSummary is None:
            prevSummary = MonthlySummary(prevMonth, 0, 0, 0)

        from utils.value_formatter import getShortMoneyString
        incomeCategories = self.transactionManager.getMonthlyCategoriesAmounts(curMonth, 0)
        expenseCategories = self.transactionManager.getMonthlyCategoriesAmounts(curMonth, 1)

        fnt = QFont("Segoe UI", 14, QFont.Weight.Bold)
        self.ui.incomePieChart.setData(incomeCategories)
        self.ui.incomePieChart.setCenterText(getShortMoneyString(curSummary.total_income), fnt, QColor("#27AE60"))
        self.ui.incomePieChart.setTitle("Thu nhập", QFont("Segoe UI", 12, QFont.Weight.Bold), QColor("#27AE60"))
        self.ui.expensePieChart.setData(expenseCategories)
        self.ui.expensePieChart.setCenterText(getShortMoneyString(curSummary.total_expense), fnt, QColor("#EB5757"))
        self.ui.expensePieChart.setTitle("Chi tiêu", QFont("Segoe UI", 12, QFont.Weight.Bold), QColor("#EB5757"))
        pass

    def refreshComparisionData(self):
        curDate = datetime.datetime.now()
        lastDate = curDate - datetime.timedelta(days=29)

        datas = self.transactionManager.getDailyTotalsInPeriod(lastDate, curDate)
        values = ()
        xAxisValues = []
        for i in range(30):
            day = (lastDate + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            if day not in datas:
                values += (day, 0, 0),
            else:
                income, expense = datas[day]
                values += (day, income, expense),

        
        for i in range(0, 30, 5):
            day = lastDate + datetime.timedelta(days=i)
            xAxisValues.append(day.strftime("%d/%m"))
        xAxisValues.append(curDate.strftime("%d/%m"))
        self.ui.cmpChart.setData(values, xAxisValues, "Ngày")        
    
    def refreshTransactionData(self):
        transactions = self.transactionManager.getTransactions(limit=30)
        self.ui.allTransTab.loadTransactions(transactions)
        self.ui.incomeTransTab.loadTransactions([t for t in transactions if t.type == 0])
        self.ui.expenseTransTab.loadTransactions([t for t in transactions if t.type == 1])

    def hideEvent(self, event):
        super().hideEvent(event)
        self.cleanData()
        
    