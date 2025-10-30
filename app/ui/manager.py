from PySide6.QtWidgets import QWidget, QApplication, QDialog
from ui.manager_ui import Ui_ManagerPage
from ui.widgets.transaction_editor import TransactionEditor
from ui.widgets.transaction_finder import TransactionFinder

class ManagerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.transactionManager = QApplication.instance().getTransactionManager()
        self.ui = Ui_ManagerPage()
        self.ui.setupUi(self)

        self.ui.addIncomeBtn.clicked.connect(self.onAddIncomeClicked)
        self.ui.addExpenseBtn.clicked.connect(self.onAddExpenseClicked)
        self.ui.findBtn.clicked.connect(self.onFindTransactionClicked)
           
        self.ui.calendar.onDateSelected = self.onCalendarDateSelected
        self.ui.calendar.updateCalendar()

        self.ui.incomeTab.setEditable(True)
        self.ui.expenseTab.setEditable(True)

    def onCalendarDateSelected(self, date):
        if date is None:
            self.ui.incomeTab.clearTransactions()
            self.ui.expenseTab.clearTransactions()
            return
        
        transactions = self.transactionManager.getTransactions(startDate=date, endDate=date)
        self.ui.incomeTab.loadTransactions([t for t in transactions if t.type == 1])
        self.ui.expenseTab.loadTransactions([t for t in transactions if t.type == 0])

    def onAddIncomeClicked(self):
        dialog = TransactionEditor(self, transactionType=0, editMode=True)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.ui.calendar.updateCalendar()
            self.onCalendarDateSelected(None)
    
    def onAddExpenseClicked(self):
        dialog = TransactionEditor(self, transactionType=1, editMode=True)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.ui.calendar.updateCalendar()
            self.onCalendarDateSelected(None)

    def onFindTransactionClicked(self):
        dialog = TransactionFinder(self)
        dialog.exec()
        self.ui.calendar.updateCalendar()
        self.onCalendarDateSelected(None)
            