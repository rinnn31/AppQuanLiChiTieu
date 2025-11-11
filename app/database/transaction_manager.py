import sqlite3
from typing import Optional
from datetime import date
from PySide6.QtCore import QThread, Signal

from app.database.transaction import MonthlySummary, Transaction

import os

class TransactionQueryThread(QThread):
    onResultReady = Signal(object)

    def __init__(self, queryFunction, *args, **kwargs):
        super().__init__()
        self._queryFunction = queryFunction
        self._args = args
        self._kwargs = kwargs

    def run(self):
        self.onResultReady.emit(self._queryFunction(*self._args, **self._kwargs))


class TransactionManager:
    TRANSACTION_DB_PATH = "data/transactions.db"

    def __init__(self):
        
        # Tạo thư mục chứa database nếu chưa tồn tại
        os.makedirs(os.path.dirname(self.TRANSACTION_DB_PATH), exist_ok=True)
        
        # Kết nối đến cơ sở dữ liệu (tự tạo mới nếu chưa có)
        self.conn = sqlite3.connect(self.TRANSACTION_DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Truy cập cột theo tên thay vì index
        
        self._createAllNecessaryTables()

    def _createAllNecessaryTables(self):
        #executescript: thực hiện nhiều lệnh cùng 1 lúc 
        self.conn.executescript(''' 
        
            -- Tạo bảng transcations (lưu các giao dịch) nếu chưa có
                CREATE TABLE IF NOT EXISTS transactions ( 
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    note TEXT,
                    category TEXT,
                    type INTEGER NOT NULL CHECK (type IN (0, 1)));
                                
            -- Tạo bảng tổng hợp giao dịch theo tháng 
                CREATE TABLE IF NOT EXISTS monthly_summaries (
                    month TEXT PRIMARY KEY,
                    total_income INTEGER NOT NULL,
                    total_expense INTEGER NOT NULL,
                    transaction_count INTEGER NOT NULL);
                                
            -- Trigger tự động cập nhật tháng khi có giao dịch mới . Khi thêm giao dịch mới:
                -- Nếu tháng đó chưa có => thêm dòng mới 
                -- Nếu đã có  => Cập nhật (UPDATE) tổng thu chi và số lượng giao dịch
                CREATE TRIGGER IF NOT EXISTS after_insert_transaction AFTER INSERT ON transactions
                BEGIN
                    INSERT INTO monthly_summaries (month, total_income, total_expense, transaction_count)
                    VALUES (strftime('%Y-%m', NEW.date), 
                            CASE WHEN NEW.type = 0 THEN NEW.amount ELSE 0 END,
                            CASE WHEN NEW.type = 1 THEN NEW.amount ELSE 0 END,
                            1)
                    ON CONFLICT(month) DO UPDATE SET
                        total_income = total_income + CASE WHEN NEW.type = 0 THEN NEW.amount ELSE 0 END,
                        total_expense = total_expense + CASE WHEN NEW.type = 1 THEN NEW.amount ELSE 0 END,
                        transaction_count = transaction_count + 1;
                                
                END;
                -- Trigger tự động trừ số tiền và số giao dịch sau khi xóa một giao dịch
                                         
                CREATE TRIGGER IF NOT EXISTS after_delete_transaction AFTER DELETE ON transactions
                BEGIN
                    UPDATE monthly_summaries
                    SET total_income = total_income - CASE WHEN OLD.type = 0 THEN OLD.amount ELSE 0 END,
                        total_expense = total_expense - CASE WHEN OLD.type = 1 THEN OLD.amount ELSE 0 END,
                        transaction_count = transaction_count - 1
                    WHERE month = strftime('%Y-%m', OLD.date);
                    
                    DELETE FROM monthly_summaries
                    WHERE month = strftime('%Y-%m', OLD.date) AND transaction_count <= 0;
                END;
                          
                CREATE TRIGGER IF NOT EXISTS after_update_transaction AFTER UPDATE ON transactions
                BEGIN
                    -- Cập nhật bản tóm tắt của tháng cũ
                    UPDATE monthly_summaries
                    -- Cập nhật của tháng mới (nếu chỉ thay đổi ngày => Tháng mới + thêm số tiền mới cập nhật vừa bị trừ)
                    SET total_income = total_income - CASE WHEN OLD.type = 0 THEN OLD.amount ELSE 0 END,
                        total_expense = total_expense - CASE WHEN OLD.type = 1 THEN OLD.amount ELSE 0 END,
                        transaction_count = transaction_count - 1
                    WHERE month = strftime('%Y-%m', OLD.date);
                    -- Nếu tháng mới chưa có thống kê → thêm mới
                    INSERT INTO monthly_summaries (month, total_income, total_expense, transaction_count)
                    VALUES (strftime('%Y-%m', NEW.date), 
                            CASE WHEN NEW.type = 0 THEN NEW.amount ELSE 0 END,
                            CASE WHEN NEW.type = 1 THEN NEW.amount ELSE 0 END,
                            1)
                    ON CONFLICT(month) DO UPDATE SET
                        total_income = total_income + CASE WHEN NEW.type = 0 THEN NEW.amount ELSE 0 END,
                        total_expense = total_expense + CASE WHEN NEW.type = 1 THEN NEW.amount ELSE 0 END,
                        transaction_count = transaction_count + 1;
                END;
                ''')
        self.conn.commit()
    
    def addTransaction(self, transaction: Transaction):
        '''
        Thêm một giao dịch mới vào cơ sở dữ liệu.
        '''

        # Sử dụng placeholder ? để tránh SQL Injection
        self.conn.execute(f'''
                INSERT INTO transactions (date, amount, note, category, type)
                VALUES (?, ?, ?, ?, ?)
                ''', (transaction.date, transaction.amount, transaction.note, transaction.category, transaction.type))
        self.conn.commit()
        
    def addTransactions(self, transactions: list[Transaction]):
        '''
        Thêm nhiều giao dịch cùng lúc vào cơ sở dữ liệu.
        '''
        datas = [(t.date, t.amount, t.note, t.category, t.type) for t in transactions]
        self.conn.executemany('''
                INSERT INTO transactions (date, amount, note, category, type)
                VALUES (?, ?, ?, ?, ?)
                ''', datas)
        self.conn.commit()

    def updateTransaction(self, transaction: Transaction):
        '''
        Cập nhật thông tin của một giao dịch đã tồn tại.
        '''
        self.conn.execute('''
                UPDATE transactions
                SET date = ?, amount = ?, note = ?, category = ?
                WHERE id = ?
                ''', (transaction.date, transaction.amount, transaction.note, transaction.category, transaction.id))
        self.conn.commit()
        pass

    def deleteTransaction(self, transaction_id: int):
        '''
        Xoá một giao dịch khỏi cơ sở dữ liệu dựa trên ID.
        '''
        self.conn.execute('''
                DELETE FROM transactions
                WHERE id = ?
                ''', (transaction_id,))
        self.conn.commit()

    def getTransactionById(self, transaction_id: int) -> Transaction | None:
        '''
        Lấy thông tin một giao dịch dựa trên ID.
        '''
        cursor = self.conn.execute('''
                SELECT * FROM transactions
                WHERE id = ?
                ''', (transaction_id,))
        
        row = cursor.fetchone()
        if row:
            return Transaction(id=row['id'], date=row['date'], amount=row['amount'], note=row['note'], category=row['category'], type=row['type'])
        return None
    

    def getTransactions(self, limit: Optional[int] = None, startDate: Optional[date] = None, endDate: Optional[date] = None, keyword: Optional[str] = None) -> list[Transaction]:
        '''
        Lấy danh sách giao dịch với các điều kiện lọc tùy chọn.
        '''
        
        query = 'SELECT * FROM transactions'
        conditions = []
        if startDate:
            conditions.append(f"date >= '{startDate.strftime('%Y-%m-%d')}'")
        if endDate:
            conditions.append(f"date <= '{endDate.strftime('%Y-%m-%d')}'")
        if keyword:
            like_pattern = f"%{keyword}%"
            conditions.append(f"(note LIKE '{like_pattern}' OR category LIKE '{like_pattern}')")

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions) # Where date > "2023-12-23" AND date < "2023-12-30" AND note LIKE "%feefef%"

        query += ' ORDER BY date DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        return [Transaction(id=row['id'], date=row['date'], amount=row['amount'], note=row['note'], category=row['category'], type=row['type']) for row in rows]
    
    def getMonthlySummary(self, month: str) -> Optional[MonthlySummary]:
        '''
        Lấy tóm tắt giao dịch trong một tháng cụ thể (thu nhập, chi tiêu, số lượng giao dịch).

        Parameters:
        month: Month in "YYYY-MM" format.

        Returns:
        Đối tượng MonthlySummary hoặc None nếu không có dữ liệu cho tháng đó.
        '''
        query = 'SELECT * FROM monthly_summaries WHERE month = ?'
        cursor = self.conn.execute(query, (month,))
        row = cursor.fetchone()
        if row:
            return MonthlySummary(month=row['month'], total_income=row['total_income'], total_expense=row['total_expense'], transaction_count=row['transaction_count'])
        return MonthlySummary(month=month, total_income=0, total_expense=0, transaction_count=0)
    
    def getDailyTotalsInPeriod(self, startDate: date, endDate: date) -> dict[str, tuple[int, int]]:
        '''
        Lấy tổng thu nhập và chi tiêu hàng ngày trong một khoảng thời gian cụ thể.

        Parameters:
        startDate: Ngày bắt đầu.
        endDate: Ngày kết thúc.

        Returns:
        Một dictionary với key là ngày theo định dạng "YYYY-MM-DD" và value là tuple (tổng thu nhập, tổng chi tiêu). Những ngày không có giao dịch sẽ không xuất hiện trong kết quả.
        
        {
            "2023-12-01": (5000000, 2000000),
        }
        '''
        query = '''
                SELECT strftime('%Y-%m-%d', date) as day,
                       SUM(CASE WHEN type = 0 THEN amount ELSE 0 END) as total_income,
                       SUM(CASE WHEN type = 1 THEN amount ELSE 0 END) as total_expense
                FROM transactions
                WHERE date BETWEEN ? AND ?
                GROUP BY day
                '''
        cursor = self.conn.execute(query, (startDate.strftime('%Y-%m-%d'), endDate.strftime('%Y-%m-%d')))
        rows = cursor.fetchall()

        return { row['day'] : (row['total_income'], row['total_expense']) for row in rows }

    def getMonthlyCategoriesAmounts(self, month: str, type: int) -> dict[str, int]:
        '''
        Lấy tổng số tiền theo từng danh mục trong một tháng cụ thể.

        Parameters:
        month: Tháng theo định dạng "YYYY-MM".
        type: 0 cho thu nhập, 1 cho chi tiêu.

        '''
        query = '''
                SELECT category, SUM(amount) as total_amount
                FROM transactions
                WHERE strftime('%Y-%m', date) = ? AND type = ?
                GROUP BY category
                '''
        cursor = self.conn.execute(query, (month, type))
        rows = cursor.fetchall()
        return {row['category']: row['total_amount'] for row in rows}

    def getDailyTotalsInMonth(self, month: str) -> dict[int, tuple[int, int]]:
        '''
        Lấy tổng thu nhập và chi tiêu hàng ngày trong một tháng cụ thể.

        Parameters:
        month: Tháng theo định dạng "YYYY-MM".

        Returns:
        Một dictionary với key là ngày (1-31) và value là tuple (tổng thu nhập, tổng chi tiêu). Những ngày không có giao dịch sẽ không xuất hiện trong kết quả.
        
        '''
        query = '''
                SELECT strftime('%d', date) as day,
                       SUM(CASE WHEN type = 0 THEN amount ELSE 0 END) as total_income,
                       SUM(CASE WHEN type = 1 THEN amount ELSE 0 END) as total_expense
                FROM transactions
                WHERE strftime('%Y-%m', date) = ?
                GROUP BY day
                '''
        cursor = self.conn.execute(query, (month,))
        rows = cursor.fetchall()
        return {int(row['day']): (row['total_income'], row['total_expense']) for row in rows}
    
    def __del__(self):
        self.conn.close()