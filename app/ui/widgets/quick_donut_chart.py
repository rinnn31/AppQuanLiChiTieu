from functools import partial
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QMargins
from PySide6.QtCharts import QPieSeries, QChart, QChartView
from PySide6.QtGui import QPainter, QCursor, QPalette

from app.ui.widgets.modern_tooltip import ModernToolTip

class QuickDonutChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.__outerPieSeries = QPieSeries()
        self.__innerPieSeries = QPieSeries()
        self.__outerPieSeries.setLabelsVisible(False)
        self.__outerPieSeries.setPieSize(0.9)
        self.__outerPieSeries.setHoleSize(0.6)
        self.__innerPieSeries.setLabelsVisible(False)
        self.__innerPieSeries.setPieSize(0.6)
        self.__innerPieSeries.setHoleSize(0.55)

        self.__chart = QChart()
        self.__chart.addSeries(self.__outerPieSeries)
        self.__chart.addSeries(self.__innerPieSeries)
        self.__chart.legend().hide()
        self.__chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.__chart.setBackgroundVisible(False)
        self.__chart.setMargins(QMargins(0,0,0,0))

        self.__chartView = QChartView(self.__chart)
        self.__chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.__chartView.setStyleSheet("background: transparent;")
        self.__chartView.setParent(self)
        self.__chartView.move(0,0)

        self.__centerLb = QLabel()
        self.__centerLb.setAlignment(Qt.AlignCenter)
        self.__centerLb.setParent(self)
        self.__centerLb.setWordWrap(True)

    def setData(self, datas: list[dict]):
        self.__outerPieSeries.clear()
        self.__innerPieSeries.clear()
        for item in datas:
            outer_slice = self.__outerPieSeries.append(item["label"], item["value"])
            outer_slice.hovered.connect(partial(self.__onSliceHovered, outer_slice, item))
            outer_slice.setBrush(item.get("main_color", Qt.gray))
            inner_slice = self.__innerPieSeries.append("", item["value"])
            inner_slice.setBrush(item.get("sub_color", Qt.lightGray))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.__chartView.resize(self.size())      

        hole_size = self.__chartView.size() * self.__innerPieSeries.holeSize()
        self.__centerLb.setMaximumWidth(hole_size.width() * 0.9)
        self.__adjustCenterText()

    def __adjustCenterText(self):
        self.__centerLb.adjustSize()
        self.__centerLb.move((self.width() - self.__centerLb.width()) / 2, (self.height() - self.__centerLb.height()) / 2)
    
    def __toggleTooltip(self, slice, item, isHovered):
        if isHovered:
            if hasattr(slice, 'tooltip') and slice.tooltip:
                return
            
            tooltip_text = f"""
                <span style="color: black">{item['label']}:</span>
                <span style="color: {item.get('value_color', 'green')}">{item['value']}{item.get('value_suffix', '')}</span>
            """
            tooltip = ModernToolTip(tooltip_text, item.get('icon', None), self)
            cursor_pos = QCursor.pos()
            tooltip.move(cursor_pos.x() + 10, cursor_pos.y())
            tooltip.show()
            slice.tooltip = tooltip
        else:
            if hasattr(slice, 'tooltip'):
                slice.tooltip.close()
                slice.tooltip = None

    def __onSliceHovered(self, slice, item, isHovered):
        if isHovered:
            start = slice.startAngle()
            end = slice.startAngle()+slice.angleSpan()
            self.__innerPieSeries.setPieStartAngle(end)
            self.__innerPieSeries.setPieEndAngle(start+360)
        else:
            self.__innerPieSeries.setPieStartAngle(0)
            self.__innerPieSeries.setPieEndAngle(360)  

        self.__toggleTooltip(slice, item, isHovered)
        slice.setExplodeDistanceFactor(0.1)
        slice.setExploded(isHovered)

    def setCenterText(self, text: str):
        self.__centerLb.setText(text)
        self.__adjustCenterText()

    def setCenterTextFont(self, font):
        self.__centerLb.setFont(font)
        self.__adjustCenterText()

    def setCenterTextColor(self, color):
        self.__centerLb.setStyleSheet(f"color: {color.name()};")
