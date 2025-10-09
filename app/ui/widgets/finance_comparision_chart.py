from PySide6.QtCore import Qt, QMargins
from PySide6.QtWidgets import QWidget
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QAreaSeries, QValueAxis, QCategoryAxis
from PySide6.QtGui import QPainter, QBrush, QColor, QPen, QCursor
import math
from ui.widgets.modern_tooltip import SummaryAmountTooltip

class FinanceComparisionChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._incomeLineSeries = QLineSeries()
        self._incomeAreaSeries = QAreaSeries(self._incomeLineSeries)
        self._incomeAreaSeries.hovered.connect(self._onHovered)
        color = QColor("#00C853")
        color.setAlpha(95)
        self._incomeAreaSeries.setPen(QPen(QColor("#00C853"), 2))
        self._incomeAreaSeries.setBrush(QBrush(color, Qt.BrushStyle.SolidPattern))

        self._expenseLineSeries = QLineSeries()
        self._expenseAreaSeries = QAreaSeries(self._expenseLineSeries)
        self._expenseAreaSeries.setPen(QPen(QColor("#D32F2F"), 2))
        self._expenseAreaSeries.hovered.connect(self._onHovered)
        color = QColor("#FF2121")
        color.setAlpha(95)
        self._expenseAreaSeries.setBrush(QBrush(color, Qt.BrushStyle.SolidPattern))

        self._chart = QChart()
        self._chart.addSeries(self._incomeAreaSeries)
        self._chart.addSeries(self._expenseAreaSeries)
        self._chart.legend().hide()
        self._chart.setBackgroundVisible(False)
        self._chart.setMargins(QMargins(0,0,0,0))
        self._chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        self._amountAxis = QValueAxis()
        self._amountAxis.setLabelFormat("%ik")
        self._amountAxis.setTitleText("Số tiền (₫))")
        self._timeAxis = None

        self._chart.addAxis(self._amountAxis, Qt.AlignLeft)
        self._incomeAreaSeries.attachAxis(self._amountAxis)
        self._expenseAreaSeries.attachAxis(self._amountAxis)

        self._chartView = QChartView(self._chart)
        self._chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._chartView.setStyleSheet("background: transparent;")
        self._chartView.setParent(self)
        self._chartView.move(0,0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._chartView.resize(self.size())
    
    def setLinePen(self, incomePen: QPen, expensePen: QPen):
        if incomePen is not None:
            self._incomeLineSeries.setPen(incomePen)
        if expensePen is not None:
            self._expenseLineSeries.setPen(expensePen)

    def setAreaBrush(self, incomeBrush: QBrush, expenseBrush: QBrush):
        if incomeBrush is not None:
            self._incomeAreaSeries.setBrush(incomeBrush)
        if expenseBrush is not None:
            self._expenseAreaSeries.setBrush(expenseBrush)

    def setTitle(self, title: str):
        self._chart.setTitle(title)

    def clearData(self):
        self._datas = None
        self._incomeLineSeries.clear()
        self._expenseLineSeries.clear()

    def setData(self, datas: list[tuple], timeAxisValues: list, timeAxisTitle: str):
        self._datas = datas

        self._incomeLineSeries.clear()
        self._expenseLineSeries.clear()
        self._chartView.repaint()
        
        for i, data in enumerate(datas, 1):
            _, income, expense = data
            self._incomeLineSeries.append(i, income / 1000)
            self._expenseLineSeries.append(i, expense / 1000)
        
        self._updateAmountAxis()

        if timeAxisValues is not None and len(timeAxisValues) > 0:
            if self._timeAxis in self._chart.axes():
                self._chart.removeAxis(self._timeAxis)

            delta = len(datas) / (len(timeAxisValues) - 1)

            self._timeAxis = QCategoryAxis()
            self._timeAxis.setGridLineVisible(False)
            self._timeAxis.setStartValue(1 - delta / 2)
            self._timeAxis.setRange(0, len(datas) + 1)
            self._timeAxis.setTitleText(timeAxisTitle)
            for i, v in enumerate(timeAxisValues):
                self._timeAxis.append(v, 1+ i * delta + delta / 2 )

            self._chart.addAxis(self._timeAxis, Qt.AlignBottom)
            self._incomeAreaSeries.attachAxis(self._timeAxis)
            self._expenseAreaSeries.attachAxis(self._timeAxis)
        

    def _updateAmountAxis(self):
        if not self._datas or len(self._datas) == 0:
            return
        maxAmount = max(max(data[1], data[2]) for data in self._datas)
        maxRange = math.ceil(maxAmount * 1.2 / 1000000) * 1000
        
        self._amountAxis.setRange(0, maxRange)
        self._amountAxis.setTickCount(5)
        
    def _onHovered(self, point, state):
        if self._datas is None or len(self._datas) == 0:
            return
        if state:
            if hasattr(self, 'tooltip') and self.tooltip:
                return
            date, income, expense = self._datas[round(point.x()) - 1]
            tooltip = SummaryAmountTooltip(date, income, expense, self)
            cursor_pos = QCursor.pos()
            tooltip.move(cursor_pos.x() - tooltip.width() / 2, cursor_pos.y() - tooltip.height() - 10)
            tooltip.show()
            self.tooltip = tooltip
        else:
            if hasattr(self, 'tooltip') and self.tooltip:
                self.tooltip.close()
                self.tooltip = None 

    