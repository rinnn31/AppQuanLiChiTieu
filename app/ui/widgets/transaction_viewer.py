from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt


class TransactionViewer(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setStyleSheet("background: white; margin: 0px;")
        self.container = QWidget()
        self.setWidget(self.container)
        self.__cachedItemCount = 0


    def loadTransactions(self, datas):
        if datas is None or len(datas) == 0:
            return
        
        self.clearTransactions()
        for data in datas:
            self.addTransaction(data)
        
    def addTransaction(self, data):
        widget = self.__createTransactionItem(data)
        widget.setStyleSheet("#transactionItem { background: white; border-radius: 5px; }")
        widget.setFixedHeight(60)
        widget.setFixedWidth(self.container.width()-40)
        widget.setParent(self.container)
        widget.move(10, 10+self.__cachedItemCount*70)
        from app.utils.window_helper import install_drop_shadow
        install_drop_shadow(widget, radius=10, color=Qt.GlobalColor.gray, offset=(0,0))
        self.container.setMinimumHeight((self.__cachedItemCount+1)*70 + 20)
        self.__cachedItemCount += 1
    
    def clearTransactions(self):
        for item in self.container.findChildren(QWidget, "transactionItem"):
            item.setParent(None)
            item.deleteLater()
        self.__cachedItemCount = 0

    def __createTransactionItem(self, data):
        widget = QWidget()
        widget.setObjectName("transactionItem")
        layout = QHBoxLayout(widget)

        from app.utils.transaction import getIconForCategory, getSubColorForCategory, getColorForType
        icon_pixmap = QPixmap(getIconForCategory(data["category"]))
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setPixmap(icon_pixmap.scaled(28,28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setStyleSheet(f"background: {getSubColorForCategory(data['category'])}; border-radius: 5px; padding: 0px 8px 0px 8px; margin-right:10px")

        title_label = QLabel()
        title_label.setTextFormat(Qt.TextFormat.RichText)
        title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_label.setText(f"<b style='color: black'>{data["category"]}</b><br><span style='color: {getColorForType(data["type"])}'>{data['value']} VND</span>")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addStretch(1)

        return widget
    
    def resizeEvent(self, arg__1):
        super().resizeEvent(arg__1)
        self.container.setFixedWidth(self.width())
        for index, item in enumerate(self.container.findChildren(QWidget, "transactionItem")):
            item.setFixedWidth(self.container.width()-40)
            item.move(10, 10+index*70)