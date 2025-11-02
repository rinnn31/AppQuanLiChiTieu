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

        self._outerPieSeries = QPieSeries()
        self._innerPieSeries = QPieSeries()
        self._outerPieSeries.setLabelsVisible(False)
        self._outerPieSeries.setPieSize(0.8) # 0 -> 1 
        self._outerPieSeries.setHoleSize(0.5)
        self._innerPieSeries.setLabelsVisible(False)
        self._innerPieSeries.setPieSize(0.5)
        self._innerPieSeries.setHoleSize(0.45)

        self._chart = QChart()
        self._chart.addSeries(self._outerPieSeries)
        self._chart.addSeries(self._innerPieSeries)
        self._chart.legend().hide()
        self._chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self._chart.setBackgroundVisible(False)
        self._chart.layout().setContentsMargins(0,0,0,0)
        self._chart.setMargins(QMargins(0,0,0,0))

        self._chartView = QChartView(self._chart)
        self._chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._chartView.setStyleSheet("background: transparent;")
        self._chartView.setParent(self)
        layout.addWidget(self._chartView)

        self._centerLb = QLabel()
        self._centerLb.setAlignment(Qt.AlignCenter)
        self._centerLb.setParent(self)
        self._centerLb.setWordWrap(True)

        self._titleLb = QLabel()
        self._titleLb.setAlignment(Qt.AlignCenter)
        self._titleLb.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(self._titleLb)
        self._titleLb.setText("Title")

    def clearData(self):
        self._innerPieSeries.clear()
        self._outerPieSeries.clear()

    
    def setData(self, datas: dict[str, int]):
        self._outerPieSeries.clear()
        self._innerPieSeries.clear()

        if datas is None or len(datas) == 0:
            outerSlice = self._outerPieSeries.append("", 1)
            outerSlice.setBrush(QColor("#E0E0E0"))
            innerSlice = self._innerPieSeries.append("", 1)
            innerSlice.setBrush(QColor("#BDBDBD"))
            return
        
        for category in datas:
            if datas[category] <= 0:
                continue
            outerSlice = self._outerPieSeries.append(category, datas[category])
            outerSlice.hovered.connect( partial(self._onSliceHovered, outerSlice, (category, datas[category])))
            outerSlice.setBrush(QColor(getMainColorForCategory(category)))

            innerSlice = self._innerPieSeries.append(category, datas[category])
            innerSlice.setBrush(QColor(getSubColorForCategory(category)))
        self._chart.scene().update()

    def resizeEvent(self, event):
        super().resizeEvent(event)  
        self._adjustCenterText()

    def _adjustCenterText(self):
        holeSize = self._chartView.size() * self._innerPieSeries.holeSize()
        self._centerLb.setMaximumWidth(holeSize.width() * 0.9)
        self._centerLb.adjustSize()
        self._centerLb.move((self._chartView.width() - self._centerLb.width()) / 2, (self._chartView.height() - self._centerLb.height()) / 2)
    
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
        if isHovered and len(self._outerPieSeries.slices()) > 1:
            start = slice.startAngle()
            end = slice.startAngle()+slice.angleSpan()
            self._innerPieSeries.setPieStartAngle(end)
            self._innerPieSeries.setPieEndAngle(start+360)
        else:
            self._innerPieSeries.setPieStartAngle(0)
            self._innerPieSeries.setPieEndAngle(360)  

        self._toggleTooltip(slice, item, isHovered)
    

    def setCenterText(self, text: str, font: QFont = None, color: QColor = None):
        self._centerLb.setText(text)
        if font is not None:
            self._centerLb.setFont(font)
        if color is not None:
            self._centerLb.setStyleSheet(f"color: {color.name()};")
        self._adjustCenterText()
        
    def setTitle(self, title: str, font: QFont = None, color: QColor = None):
        self._titleLb.setText(title)
        if font is not None:
            self._titleLb.setFont(font)
        if color is not None:
            self._titleLb.setStyleSheet(f"color: {color.name()};")
        