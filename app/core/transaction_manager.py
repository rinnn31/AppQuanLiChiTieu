import sqlite3
from typing import Optional
from datetime import date
from core.transaction import MonthlySummary, Transaction


class TransactionManager:
    TRANSACTION_DB_PATH = "transactions.db"

    def __init__(self):
        # Kết nối đến cơ sở dữ liệu tại đường dẫn TRANSACTION_DB_PATH, nếu không tồn tại sẽ tự tạo mới
        self.conn = sqlite3.connect(self.TRANSACTION_DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        self._createAllNecessaryTables()

    def _createAllNecessaryTables(self):
        self.conn.executescript('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    note TEXT,
                    category TEXT,
                    type INTEGER NOT NULL CHECK (type IN (0, 1)));
                
                CREATE TABLE IF NOT EXISTS monthly_transaction_summaries (
                    month TEXT PRIMARY KEY,
                    total_income REAL NOT NULL,
                    total_expense REAL NOT NULL,
                    transaction_count INTEGER NOT NULL);
                
                CREATE TRIGGER IF NOT EXISTS after_insert_transaction AFTER INSERT ON transactions
                BEGIN
                    INSERT INTO monthly_transaction_summaries (month, total_income, total_expense, transaction_count)
                    VALUES (strftime('%Y-%m', NEW.date), 
                            CASE WHEN NEW.type = 0 THEN NEW.amount ELSE 0 END,
                            CASE WHEN NEW.type = 1 THEN NEW.amount ELSE 0 END,
                            1)
                    ON CONFLICT(month) DO UPDATE SET
                        total_income = total_income + CASE WHEN NEW.type = 0 THEN NEW.amount ELSE 0 END,
                        total_expense = total_expense + CASE WHEN NEW.type = 1 THEN NEW.amount ELSE 0 END,
                        transaction_count = transaction_count + 1;
                                
                END;
                          
                CREATE TRIGGER IF NOT EXISTS after_delete_transaction AFTER DELETE ON transactions
                BEGIN
                    UPDATE monthly_transaction_summaries
                    SET total_income = total_income - CASE WHEN OLD.type = 0 THEN OLD.amount ELSE 0 END,
                        total_expense = total_expense - CASE WHEN OLD.type = 1 THEN OLD.amount ELSE 0 END,
                        transaction_count = transaction_count - 1
                    WHERE month = strftime('%Y-%m', OLD.date);
                    
                    DELETE FROM monthly_transaction_summaries
                    WHERE month = strftime('%Y-%m', OLD.date) AND transaction_count <= 0;
                END;
                          
                CREATE TRIGGER IF NOT EXISTS after_update_transaction AFTER UPDATE ON transactions
                BEGIN
                    -- Cập nhật bản tóm tắt của tháng cũ, nếu ngày đã thay đổi 
                    UPDATE monthly_transaction_summaries
                    SET total_income = total_income - CASE WHEN OLD.type = 0 THEN OLD.amount ELSE 0 END + CASE WHEN NEW.type = 0 THEN NEW.amount ELSE 0 END,
                        total_expense = total_expense - CASE WHEN OLD.type = 1 THEN OLD.amount ELSE 0 END + CASE WHEN NEW.type = 1 THEN NEW.amount ELSE 0 END
                    WHERE month = strftime('%Y-%m', OLD.date);
                    
                    UPDATE monthly_transaction_summaries
                    SET total_income = total_income + CASE WHEN NEW.type = 0 THEN NEW.amount ELSE 0 END,
                        total_expense = total_expense + CASE WHEN NEW.type = 1 THEN NEW.amount ELSE 0 END,
                        transaction_count = transaction_count + 1
                    WHERE month = strftime('%Y-%m', NEW.date) AND month != strftime('%Y-%m', OLD.date);
                    
                    INSERT INTO monthly_transaction_summaries (month, total_income, total_expense, transaction_count)
                    SELECT strftime('%Y-%m', NEW.date), 
                           CASE WHEN NEW.type = 0 THEN NEW.amount ELSE 0 END,
                           CASE WHEN NEW.type = 1 THEN NEW.amount ELSE 0 END,
                           1
                    WHERE NOT EXISTS (SELECT 1 FROM monthly_transaction_summaries WHERE month = strftime('%Y-%m', NEW.date));
                END;
                ''')
        self.conn.commit()
    
    def addTransaction(self, transaction: Transaction):
        self.conn.execute(f'''
                INSERT INTO transactions (date, amount, note, category, type)
                VALUES (?, ?, ?, ?, ?)
                ''', (transaction.date, transaction.amount, transaction.note, transaction.category, transaction.type))
        self.conn.commit()
        
    def addTransactions(self, transactions: list[Transaction]):
        datas = [(t.date, t.amount, t.note, t.category, t.type) for t in transactions]
        self.conn.executemany('''
                INSERT INTO transactions (date, amount, note, category, type)
                VALUES (?, ?, ?, ?, ?)
                ''', datas)
        self.conn.commit()

    def updateTransaction(self, transaction: Transaction):
        self.conn.execute('''
                UPDATE transactions
                SET date = ?, amount = ?, note = ?, category = ?
                WHERE id = ?
                ''', (transaction.date, transaction.amount, transaction.note, transaction.category, transaction.id))
        self.conn.commit()
        pass

    def deleteTransaction(self, transaction_id: int):
        self.conn.execute('''
                DELETE FROM transactions
                WHERE id = ?
                ''', (transaction_id,))
        self.conn.commit()

    def getTransactionById(self, transaction_id: int) -> Transaction | None:
        cursor = self.conn.execute('''
                SELECT * FROM transactions
                WHERE id = ?
                ''', (transaction_id,))
        
        row = cursor.fetchmany()
        if row:
            return Transaction(_id=row['id'], date=row['date'], amount=row['amount'], note=row['note'], category=row['category'], type=row['type'])
        return None
    

    def getTransactions(self, limit: Optional[int] = None, startDate: Optional[date] = None, endDate: Optional[date] = None, keyword: Optional[str] = None) -> list[Transaction]:
        # Lấy danh giao dịch với các điều kiện lọc tùy chọn
        
        query = 'SELECT * FROM transactions'
        conditions = []
        ['date > "12-23 AND date < "2023-12-30" AND note Lkfeefef']
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
        return [Transaction(_id=row['id'], date=row['date'], amount=row['amount'], note=row['note'], category=row['category'], type=row['type']) for row in rows]
    
    def getMonthlySummary(self, month: str) -> Optional[MonthlySummary]:
        '''
        Lấy tóm tắt giao dịch trong một tháng cụ thể (thu nhập, chi tiêu, số lượng giao dịch).

        Parameters:
        month: Month in "YYYY-MM" format.

        Returns:
        Đối tượng MonthlySummary hoặc None nếu không có dữ liệu cho tháng đó.
        '''
        query = 'SELECT * FROM monthly_transaction_summaries WHERE month = ?'
        cursor = self.conn.execute(query, (month,))
        row = cursor.fetchone()
        if row:
            return MonthlySummary(month=row['month'], total_income=row['total_income'], total_expense=row['total_expense'], transaction_count=row['transaction_count'])
        return None
    
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