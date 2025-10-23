from functools import partial
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QMargins
from PySide6.QtCharts import QPieSeries, QChart, QChartView
from PySide6.QtGui import QPainter, QCursor, QColor, QFont

from ui.widgets.modern_tooltip import CategoryAmountTooltip
from utils.transaction_style import getMainColorForCategory, getSubColorForCategory, getIconForCategory

class CategoryDonutChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(4)

        self.outerPieSeries = QPieSeries()
        self.innerPieSeries = QPieSeries()
        self.outerPieSeries.setLabelsVisible(False)
        self.outerPieSeries.setPieSize(0.9)
        self.outerPieSeries.setHoleSize(0.6)
        self.innerPieSeries.setLabelsVisible(False)
        self.innerPieSeries.setPieSize(0.6)
        self.innerPieSeries.setHoleSize(0.55)

        self.chart = QChart()
        self.chart.addSeries(self.outerPieSeries)
        self.chart.addSeries(self.innerPieSeries)
        self.chart.legend().hide()
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.setBackgroundVisible(False)
        self.chart.layout().setContentsMargins(0,0,0,0)
        self.chart.setMargins(QMargins(0,0,0,0))

        self.chartView = QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chartView.setStyleSheet("background: transparent;")
        self.chartView.setParent(self)
        layout.addWidget(self.chartView)

        self.centerLb = QLabel()
        self.centerLb.setAlignment(Qt.AlignCenter)
        self.centerLb.setParent(self)
        self.centerLb.setWordWrap(True)

        self.titleLb = QLabel()
        self.titleLb.setAlignment(Qt.AlignCenter)
        self.titleLb.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(self.titleLb)
        self.titleLb.setText("Title")

    def clearData(self):
        self.innerPieSeries.clear()
        self.outerPieSeries.clear()


    def setData(self, datas: dict[str, int]):

        self.outerPieSeries.clear()
        self.innerPieSeries.clear()

        if datas is None or len(datas) == 0:
            outerSlice = self.outerPieSeries.append("", 1)
            outerSlice.setBrush(QColor("#E0E0E0"))
            innerSlice = self.innerPieSeries.append("", 1)
            innerSlice.setBrush(QColor("#BDBDBD"))
            return
        for category in datas:
            outerSlice = self.outerPieSeries.append(category, datas[category])
            outerSlice.hovered.connect(partial(self._onSliceHovered, outerSlice, (category, datas[category])))
            outerSlice.setBrush(QColor(getMainColorForCategory(category)))
            innerSlice = self.innerPieSeries.append(category, datas[category])
            innerSlice.setBrush(QColor(getSubColorForCategory(category)))
        self.chart.scene().update()

    def resizeEvent(self, event):
        super().resizeEvent(event)  
        self._adjustCenterText()

    def _adjustCenterText(self):
        holeSize = self.chartView.size() * self.innerPieSeries.holeSize()
        self.centerLb.setMaximumWidth(holeSize.width() * 0.9)
        self.centerLb.adjustSize()
        self.centerLb.move((self.chartView.width() - self.centerLb.width()) / 2, (self.chartView.height() - self.centerLb.height()) / 2)
    
    def _toggleTooltip(self, slice, item, isHovered):
        if isHovered:
            if hasattr(slice, 'tooltip') and slice.tooltip:
                return
            
            tooltip = CategoryAmountTooltip(item[0], item[1], self)
            cursorPos = QCursor.pos()
            tooltip.move(cursorPos.x() + 10, cursorPos.y())
            tooltip.show()
            slice.tooltip = tooltip
        else:
            if hasattr(slice, 'tooltip'):
                slice.tooltip.close()
                slice.tooltip = None

    def _onSliceHovered(self, slice, item, isHovered):
        if isHovered:
            start = slice.startAngle()
            end = slice.startAngle()+slice.angleSpan()
            self.innerPieSeries.setPieStartAngle(end)
            self.innerPieSeries.setPieEndAngle(start+360)
        else:
            self.innerPieSeries.setPieStartAngle(0)
            self.innerPieSeries.setPieEndAngle(360)  

        self._toggleTooltip(slice, item, isHovered)
        slice.setExplodeDistanceFactor(0.1)
        slice.setExploded(isHovered)

    def setCenterText(self, text: str, font: QFont = None, color: QColor = None):
        self.centerLb.setText(text)
        if font is not None:
            self.centerLb.setFont(font)
        if color is not None:
            self.centerLb.setStyleSheet(f"color: {color.name()};")
        self._adjustCenterText()
        
    def setTitle(self, title: str, font: QFont = None, color: QColor = None):
        self.titleLb.setText(title)
        if font is not None:
            self.titleLb.setFont(font)
        if color is not None:
            self.titleLb.setStyleSheet(f"color: {color.name()};")
        