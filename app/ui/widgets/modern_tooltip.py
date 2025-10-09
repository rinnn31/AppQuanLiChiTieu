from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QFont

from utils.window_helper import applyDropShadow
from utils.transaction_style import getColorForType, getIconForCategory, getMainColorForCategory
class ModernTooltip(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)   
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.tooltipBackground = QWidget(self)
        self.tooltipBackground.setObjectName("tooltip_bg")
        self.tooltipBackground.setStyleSheet("""
            #tooltip_bg {
                background-color: white;
                border-radius: 4px;
            }""")
        self.adjustBackgroundSize()
        applyDropShadow(self.tooltipBackground, radius=10, offset=(0, 0))
    
    def adjustBackgroundSize(self):
        self.tooltipBackground.adjustSize()
        self.resize(self.tooltipBackground.size() + QSize(10, 10))
        self.tooltipBackground.move(5,5)

class CategoryAmountTooltip(ModernTooltip):
    DEFAULT_FONT_SIZE = 12
    DEFAULT_ICON_SIZE = 32

    def __init__(self, category: str, amount: float, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self.tooltipBackground)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        icon_pix = QPixmap(getIconForCategory(category)).scaled(self.DEFAULT_ICON_SIZE, self.DEFAULT_ICON_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._icon_lb = QLabel()
        self._icon_lb.setPixmap(icon_pix)
        layout.addWidget(self._icon_lb)
            
        self._text_lb = QLabel(f'<span style="color: black;">{category}: </span><span style="color: {getMainColorForCategory(category)};">{amount:,.0f} ₫</span>')
        self._text_lb.setFont(QFont("Segoe UI", self.DEFAULT_FONT_SIZE, QFont.Weight.Bold))
        self._text_lb.setTextFormat(Qt.TextFormat.RichText)
        self._text_lb.adjustSize()
        layout.addWidget(self._text_lb)

        self.adjustBackgroundSize()

class SummaryAmountTooltip(ModernTooltip):
    DEFAULT_FONT_SIZE = 12

    def __init__(self, date: str, totalIncome : int, totalExpense: int, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self.tooltipBackground)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)
        
        text = f'''<span style="color: black;">{date}</span><br>
                <span style="color: {getColorForType(0)};">Tổng thu: {totalIncome:,} ₫</span><br>
                <span style="color: {getColorForType(1)};">Tổng chi: {totalExpense:,} ₫</span>'''
        self._text_lb = QLabel(text)
        self._text_lb.setFont(QFont("Segoe UI", self.DEFAULT_FONT_SIZE, QFont.Weight.Bold))
        self._text_lb.setTextFormat(Qt.TextFormat.RichText)
        self._text_lb.adjustSize()
        layout.addWidget(self._text_lb)

        self.adjustBackgroundSize()