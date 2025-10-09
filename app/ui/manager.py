from PySide6.QtWidgets import QWidget
from core.transaction_manager import TransactionManager
from ui.manager_ui import Ui_ManagerPage
from ui.widgets.transaction_editor import TransactionEditor
from ui.widgets.transaction_finder import TransactionFinder

class ManagerPage(QWidget):
    def __init__(self, transactionManager: TransactionManager):
        super().__init__()
        self._transactionManager = transactionManager
        self.ui = Ui_ManagerPage()
        self.ui.setupUi(self)

        self.ui.addIncomeBtn.clicked.connect(self.onAddIncomeClicked)
        self.ui.addExpenseBtn.clicked.connect(self.onAddExpenseClicked)
        self.ui.findBtn.clicked.connect(self.onFindTransactionClicked)
        
        self.ui.calendar.setTransactionManager(self._transactionManager)    
        self.ui.calendar.onDateSelected = self.onCalendarDateSelected
        self.ui.calendar.updateCalendar()

    def onCalendarDateSelected(self, date):
        if date is None:
            self.ui.incomeTab.clearTransactions()
            self.ui.expenseTab.clearTransactions()
            return
        
        transactions = self._transactionManager.getTransactions(startDate=date, endDate=date)
        self.ui.incomeTab.loadTransactions([t for t in transactions if t.type == 0])
        self.ui.expenseTab.loadTransactions([t for t in transactions if t.type == 1])

    def onAddIncomeClicked(self):
        dialog = TransactionEditor(self, transactionType=0, editMode=True)
        dialog.exec()
    
    def onAddExpenseClicked(self):
        dialog = TransactionEditor(self, transactionType=1, editMode=True)
        dialog.exec()

    def onFindTransactionClicked(self):
        dialog = TransactionFinder(self._transactionManager, self)
        dialog.exec()