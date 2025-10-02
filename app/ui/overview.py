from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QBrush, QPen, QFont, QPixmap
from app.ui.overview_ui import Ui_OverviewPage

class OverviewPage(QWidget):
    PERIODIC_IN_WEEK = "Trong tuần"
    PERIODIC_IN_MONTH = "Trong tháng"
    PERIODIC_IN_YEAR = "Trong năm"

    COMPARISION_IN_WEEK = "Trong tuần"
    COMPARISION_IN_MONTH = "Trong tháng"
    COMPARISION_IN_3_MONTH = "Trong 3 tháng"
    COMPARISION_IN_6_MONTH = "Trong 6 tháng"
    COMPARISION_IN_YEAR = "Trong năm"


    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_OverviewPage()
        self.ui.setupUi(self)

        for item in [self.PERIODIC_IN_WEEK, self.PERIODIC_IN_MONTH, self.PERIODIC_IN_YEAR]:
            self.ui.periodicCbox.addItem(item)
        for item in [self.COMPARISION_IN_WEEK, self.COMPARISION_IN_MONTH, self.COMPARISION_IN_3_MONTH, self.COMPARISION_IN_6_MONTH, self.COMPARISION_IN_YEAR]:
            self.ui.comparisionCbox.addItem(item)

        self.refreshData()

    def refreshData(self):
        self.__refreshPeriodicData(self.ui.periodicCbox.currentText())
        self.__refreshComparisionData(self.ui.comparisionCbox.currentText())
        self.__refreshTransactionData()
        sample_pie_data = [
            {"label": "Food", "value": 500, "main_color": QColor("#FF6384"), "sub_color": QColor("#FFB1C1"), "value_color": "red"},
            {"label": "Transport", "value": 300, "main_color": QColor("#36A2EB"), "sub_color": QColor("#9AD0F5"), "value_color": "blue"},
            {"label": "Entertainment", "value": 200, "main_color": QColor("#FFCE56"), "sub_color": QColor("#FFE29A"), "value_color": "orange"},
            {"label": "Utilities", "value": 150, "main_color": QColor("#4BC0C0"), "sub_color": QColor("#A8EAEA"), "value_color": "teal"},
        ]
        sample_area_data = [QPointF(x,y) for x, y in enumerate([10, 15, 8, 12, 20, 18, 25, 22, 30, 28, 35, 40])]
        sample_area_data2 = [QPointF(x,y) for x, y in enumerate([5, 8, 6, 10, 15, 12, 18, 15, 22, 20, 25, 30])]
        xAxisValues = list(range(1, 13))
        yAxisValues = [0, 10, 20, 30, 40, 50]
        pen = QPen(QColor("#00BFA6"))  # teal
        pen.setWidth(2)
        brush = QBrush(QColor(0, 191, 166, 100))
        self.ui.incomeAreaChart.setTitle("Monthly Income")
        self.ui.incomeAreaChart.setAreaPen(pen)
        self.ui.incomeAreaChart.setAreaBrush(brush)
        self.ui.incomeAreaChart.setData(sample_area_data)
        self.ui.incomeAreaChart.attachAxises(xAxisValues, yAxisValues, None, "Amount ($)", xAxisFormat="%d", yAxisFormat="%.0f")

        self.ui.expenseAreaChart.setTitle("Monthly Expense")
        self.ui.expenseAreaChart.setAreaPen(pen)
        self.ui.expenseAreaChart.setAreaBrush(brush)
        self.ui.expenseAreaChart.setData(sample_area_data2)
        self.ui.expenseAreaChart.attachAxises(xAxisValues, yAxisValues, None, "Amount ($)", xAxisFormat="%d", yAxisFormat="%.0f")

        self.ui.incomePieChart.setData(sample_pie_data)
        self.ui.incomePieChart.setCenterText("Total\n 1000$")
        self.ui.incomePieChart.setCenterTextColor(QColor("green"))
        self.ui.incomePieChart.setCenterTextFont(QFont("Segoe UI", 12, QFont.Bold))
        self.ui.expensePieChart.setData(sample_pie_data)
        self.ui.expensePieChart.setCenterText("Total\n 650$")
        self.ui.expensePieChart.setCenterTextColor(QColor("red"))
        self.ui.expensePieChart.setCenterTextFont(QFont("Segoe UI", 12, QFont.Bold))

    def __refreshPeriodicData(self, type):
        if type == self.PERIODIC_IN_WEEK:
            pass
        elif type == self.PERIODIC_IN_MONTH:
            pass
        else:
            pass

    def __refreshComparisionData(self, type):
        if type == self.COMPARISION_IN_WEEK:
            pass
        elif type == self.COMPARISION_IN_MONTH:
            pass
        elif type == self.COMPARISION_IN_3_MONTH:
            pass
        elif type == self.COMPARISION_IN_6_MONTH:
            pass
        else:
            pass
    
    def __refreshTransactionData(self):
        
        datas = [
            {"type": 0, "category": "Lương", "value": 500},
            {"type": 0, "category": "Đầu tư", "value": 300},
            {"type": 1, "category": "Ăn uống", "value": 200},
            {"type": 1, "category": "Di chuyển", "value": 150},
            {"type": 1, "category": "Giải trí", "value": 100},
            {"type": 0, "category": "Lương", "value": 500},
            {"type": 0, "category": "Đầu tư", "value": 300},
            {"type": 1, "category": "Ăn uống", "value": 200},
            {"type": 1, "category": "Di chuyển", "value": 150},
            {"type": 1, "category": "Giải trí", "value": 100},
            {"type": 0, "category": "Lương", "value": 500},
            {"type": 0, "category": "Đầu tư", "value": 300},
            {"type": 1, "category": "Ăn uống", "value": 200},
            {"type": 1, "category": "Di chuyển", "value": 150},
            {"type": 1, "category": "Giải trí", "value": 100},
            {"type": 0, "category": "Lương", "value": 500},
            {"type": 0, "category": "Đầu tư", "value": 300},
            {"type": 1, "category": "Ăn uống", "value": 200},
            {"type": 1, "category": "Di chuyển", "value": 150},
            {"type": 1, "category": "Giải trí", "value": 100},
        ]

        self.ui.allTransTab.loadTransactions(datas)
        self.ui.incomeTransTab.loadTransactions([data for data in datas if data["type"] == 0])
        self.ui.expenseTransTab.loadTransactions([data for data in datas if data["type"] == 1])
    
    def installRuntimeComponents(self):
        pass
