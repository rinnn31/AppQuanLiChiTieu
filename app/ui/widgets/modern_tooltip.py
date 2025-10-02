from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QFont

from app.utils.window_helper import install_drop_shadow

class ModernToolTip(QWidget):
    DEFAULT_FONT_SIZE = 12
    DEFAULT_ICON_SIZE = 32

    def __init__(self, text, icon = None, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)   
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        bg = QWidget(self)
        bg.setObjectName("tooltip_bg")
        bg.setStyleSheet("""
            #tooltip_bg {
                background-color: white;
                border-radius: 4px;
            }""")
        layout = QHBoxLayout(bg)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        if icon is not None:
            icon_pix = QPixmap(icon).scaled(self.DEFAULT_ICON_SIZE, self.DEFAULT_ICON_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.__icon_lb = QLabel()
            self.__icon_lb.setPixmap(icon_pix)
            layout.addWidget(self.icon_label)
            
        self.__text_lb = QLabel(text)
        self.__text_lb.setFont(QFont("Segoe UI", self.DEFAULT_FONT_SIZE, QFont.Weight.Bold))
        self.__text_lb.setTextFormat(Qt.TextFormat.RichText)
        self.__text_lb.adjustSize()
        layout.addWidget(self.__text_lb)
        
        bg.adjustSize()
        self.resize(bg.size() + QSize(10, 10))
        bg.move(5,5)
        install_drop_shadow(bg, radius=10, offset=(0, 0))


        