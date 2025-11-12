from functools import partial
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QMargins
from PySide6.QtCharts import QPieSeries, QChart, QChartView
from PySide6.QtGui import QPainter, QCursor, QColor, QFont

from ui.widgets.modern_tooltip import CategoryAmountTooltip
from utils.transaction_style import getMainColorForCategory, getSubColorForCategory, getIconForCategory

class CategoryDonutChart(QWidget): # Lớp kế thừa từ QWidget để hiện thị được lên màn hình

    def __init__(self, parent=None):
        # parent = None: là 1 Widget đọc lập có thế gắn vào Widget cha
        super().__init__(parent) # Gọi hàm khởi tạo của Widget
        # Đặt layout cho Widget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(4)

        # Tạo các vòng tròn dữ liệu chưa các Slice(QPieSlice) như: "Ăn uống" :200
        self._outerPieSeries = QPieSeries()
        self._innerPieSeries = QPieSeries()
        self._outerPieSeries.setLabelsVisible(False)
        self._outerPieSeries.setPieSize(0.9) # 0 -> 1 
        self._outerPieSeries.setHoleSize(0.6)
        self._innerPieSeries.setLabelsVisible(False)
        self._innerPieSeries.setPieSize(0.6)
        self._innerPieSeries.setHoleSize(0.55)

        # Tạo QChart để chứa các slice dữ liệu trên
        self._chart = QChart()
        self._chart.addSeries(self._outerPieSeries)
        self._chart.addSeries(self._innerPieSeries)
        self._chart.legend().hide()
        self._chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self._chart.setBackgroundVisible(False)
        self._chart.layout().setContentsMargins(0,0,0,0)
        self._chart.setMargins(QMargins(0,0,0,0))

        # Hiện thị QChart(QChartView là widget hiện thi QChart được đặt vào layout chính)
        self._chartView = QChartView(self._chart)
        self._chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._chartView.setStyleSheet("background: transparent;")
        self._chartView.setParent(self)
        layout.addWidget(self._chartView)

        # Label nằm ở giữa biểu đồ không cho layout quản lí
        self._centerLb = QLabel()
        self._centerLb.setAlignment(Qt.AlignCenter)
        self._centerLb.setParent(self)
        self._centerLb.setWordWrap(True)

        # Label được đặt trong layout để layout tự chỉnh 
        self._titleLb = QLabel()
        self._titleLb.setAlignment(Qt.AlignCenter)
        self._titleLb.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(self._titleLb)
        self._titleLb.setText("Title")

    def clearData(self):
        self._innerPieSeries.clear()
        self._outerPieSeries.clear()

    
    def setData(self, datas: dict[str, int]):
        '''
        Dạng dictionary
        datas: {
            "tieude1": 100000,
            "tieude2": 200000,
            ...}
        '''
        self._outerPieSeries.clear()
        self._innerPieSeries.clear()

        # Nếu không có dữ liệu vòng trong trg và ngoài đều là 1 và có màu xám
        if datas is None or len(datas) == 0:
            outerSlice = self._outerPieSeries.append("", 1)
            outerSlice.setBrush(QColor("#E0E0E0"))
            innerSlice = self._innerPieSeries.append("", 1)
            innerSlice.setBrush(QColor("#BDBDBD"))
            return
        
        #
        for category in datas:
            outerSlice = self._outerPieSeries.append(category, datas[category]) # outerSlice được gán bằng các QPieSilce vừa thêm vào
            outerSlice.hovered.connect( partial(self._onSliceHovered, outerSlice, (category, datas[category])))
            '''
            Signal hovered truyền đúng 1 tham số là isHovered đến hàm được connect
            Sử dụng partial để có thêm tự tạo thêm 1 hàm giống phương thức gốc(nên mới có self.) _onSliceHovered để truyền thêm 
            các đối số slice = outerSlice, item = (category,datas[category]) 
            và tham số isHovered sẽ tự được thêm vào 
            Mục đích để biết Slice nào đang được hover
            '''
            outerSlice.setBrush(QColor(getMainColorForCategory(category)))

            innerSlice = self._innerPieSeries.append(category, datas[category])
            innerSlice.setBrush(QColor(getSubColorForCategory(category)))
        self._chart.scene().update()

    def resizeEvent(self, event):
        # Cập nhập lại kích thước của các class khi phóng to hoặc thu nhỏ lại
        super().resizeEvent(event)
        # Chỉnh lại cho label nằm giữa  
        self._adjustCenterText()

    def _adjustCenterText(self):
        holeSize = self._chartView.size() * self._innerPieSeries.holeSize()
        self._centerLb.setMaximumWidth(holeSize.width() * 0.9)
        self._centerLb.adjustSize()
        self._centerLb.move((self._chartView.width() - self._centerLb.width()) / 2, (self._chartView.height() - self._centerLb.height()) / 2)
    
    def _toggleTooltip(self, slice, item, isHovered):
        if isHovered:
            '''
            Kiểm tả xem obj slice có thuộc tính tooltip và tooltip có đang hiện thị không
            nếu có thì return không tạo thêm tooltip phải ktra xem slice có tooltip chưa rồi
            mới ktra xem tooltip có đang hiện không
            '''
            if hasattr(slice, 'tooltip') and slice.tooltip:
                return
            
            tooltip = CategoryAmountTooltip(item[0], item[1], self)
            cursorPos = QCursor.pos()
            tooltip.move(cursorPos.x() + 10, cursorPos.y())
            tooltip.show()
            
            slice.tooltip = tooltip
        else:
            # Ktra cho an toàn vì có thế hover nhanh quá chưa kịp tạo tooltip nếu ko ktra sẽ bị lỗi  AttributeError
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

        self._toggleTooltip(slice, item, isHovered) # Hiện thị tooltip
        
        #Làm cho slice tách ra khi hover
        slice.setExplodeDistanceFactor(0.1)
        slice.setExploded(isHovered and len(self._outerPieSeries.slices()) > 1)

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
        