from dataclasses import dataclass

@dataclass
class Transaction:
    _id : int = -1
    amount: int = 0
    category: str = ""
    type: int  = 0
    date: str = ""
    note: str = ""
    
    def isIncomeTransaction(self):
        return self.type == 0
    
    def getDateObject(self):
        from datetime import datetime
        return datetime.strptime(self.date, "%Y-%m-%d").date()

@dataclass
class MonthlySummary:
    month: str
    total_income: int
    total_expense: int
    transaction_count: int