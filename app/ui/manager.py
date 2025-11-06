from PySide6.QtWidgets import QWidget, QApplication, QDialog
from app.ui.manager_ui import Ui_ManagerPage
from app.ui.widgets.transaction_editor import TransactionEditor
from app.ui.widgets.transaction_finder import TransactionFinder

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

        self.ui.incomeTab.onTransactionItemClicked = self.onTransactionItemClicked
        self.ui.expenseTab.onTransactionItemClicked = self.onTransactionItemClicked

    def onCalendarDateSelected(self, date):
        if date is None:
            self.ui.incomeTab.clearTransactions()
            self.ui.expenseTab.clearTransactions()
            return
        
        transactions = self.transactionManager.getTransactions(startDate=date, endDate=date)
        self.ui.incomeTab.loadTransactions([t for t in transactions if t.type == 0])
        self.ui.expenseTab.loadTransactions([t for t in transactions if t.type == 1])

    def onAddIncomeClicked(self):
        dialog = TransactionEditor(self, transactionType=0, editMode=True)
        dialog.exec()
        self.ui.calendar.updateCalendar()
        self.onCalendarDateSelected(None)
    
    def onAddExpenseClicked(self):
        dialog = TransactionEditor(self, transactionType=1, editMode=True)
        dialog.exec()
        self.ui.calendar.updateCalendar()
        self.onCalendarDateSelected(None)

    def onFindTransactionClicked(self):
        dialog = TransactionFinder(self)
        dialog.exec()
        self.ui.calendar.updateCalendar()
        self.onCalendarDateSelected(None)
        
    def onTransactionItemClicked(self, transaction):
        dialog = TransactionEditor(self, transaction.type, True, transaction.id)
        dialog.exec()
        self.ui.calendar.updateCalendar()
        self.onCalendarDateSelected(None)