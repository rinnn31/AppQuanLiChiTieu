from PySide6.QtCore import Qt, QMargins
from PySide6.QtWidgets import QWidget
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QAreaSeries, QValueAxis, QCategoryAxis
from PySide6.QtGui import QPainter, QBrush, QColor, QPen

class QuickAreaChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.__lineSeries = QLineSeries()
        self.__lineSeries.setPointsVisible(False)
        self.__areaSeries = QAreaSeries(self.__lineSeries)
        self.__areaSeries.hovered.connect(self.__onHovered)

        self.__chart = QChart()
        self.__chart.addSeries(self.__areaSeries)
        self.__chart.legend().hide()
        self.__chart.setBackgroundVisible(False)
        self.__chart.setMargins(QMargins(0,0,0,0))
        self.__chart.createDefaultAxes()

        self.__chartView = QChartView(self.__chart)
        self.__chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.__chartView.setStyleSheet("background: transparent;")
        self.__chartView.setParent(self)
        self.__chartView.move(0,0)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.__chartView.resize(self.size())
    
    def setAreaPen(self, pen: QPen):
        self.__areaSeries.setPen(pen)

    def setAreaBrush(self, brush: QBrush):
        self.__areaSeries.setBrush(brush)

    def setTitle(self, title: str):
        self.__chart.setTitle(title)
    
    def attachAxises(self, xAxisValues: list, yAxisValues: list, xAxisTitle: str = "", yAxisTitle: str = "", xAxisFormat: str = None, yAxisFormat: str = None):
        if xAxisValues[0] is str:
            xAxis = QCategoryAxis()
            xAxis.setTitleText(xAxisTitle)
            for i, v in enumerate(xAxisValues):
                xAxis.append(str(v), i)
        else:
            xAxis = QValueAxis()
            if xAxisFormat is not None:
                xAxis.setLabelFormat(xAxisFormat)
            xAxis.setTitleText(xAxisTitle)
            xAxis.setRange(min(xAxisValues), max(xAxisValues))
            xAxis.setTickCount(len(xAxisValues))
        self.__chart.setAxisX(xAxis, self.__areaSeries)

        if yAxisValues[0] is str:
            yAxis = QCategoryAxis()
            yAxis.setTitleText(yAxisTitle)
            for i, v in enumerate(yAxisValues):
                yAxis.append(str(v), i)
        else:
            yAxis = QValueAxis()
            if yAxisFormat is not None:
                yAxis.setLabelFormat(yAxisFormat)
            yAxis.setTitleText(yAxisTitle)
            yAxis.setRange(min(yAxisValues), max(yAxisValues))
            yAxis.setTickCount(len(yAxisValues))
        self.__chart.setAxisY(yAxis, self.__areaSeries)


    def setData(self, datas: list[tuple]):
        self.__lineSeries.clear()
        self.__lineSeries.append(datas)

    def __onHovered(self, point, state):
        pass

    