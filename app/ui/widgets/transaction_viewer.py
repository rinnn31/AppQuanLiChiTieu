from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QLabel, QStackedWidget, QSizePolicy, QVBoxLayout
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from ui.widgets.transaction_editor import TransactionEditor
from core.transaction import Transaction

class TransactionViewer(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setStyleSheet("background: white; margin: 0px;")
        self.verticalScrollBar().setMaximumWidth(6)

        self.emptyStateWidget = QWidget()

        emptyLayout = QVBoxLayout(self.emptyStateWidget)
        emptyLayout.setContentsMargins(0,80,0,0)
        emptyLayout.setSpacing(10)
        emptyIcon = QLabel()
        emptyIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emptyIcon.setPixmap(QPixmap(":resources/images/empty.png").scaled(120,120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        emptyIcon.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        emptyText = QLabel("Chưa có giao dịch nào")
        emptyText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emptyText.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        emptyText.setStyleSheet("color: gray")

        emptyLayout.addWidget(emptyIcon)
        emptyLayout.addWidget(emptyText)
        emptyLayout.addStretch()

        self.contentWidget = QWidget()
        layout = QVBoxLayout(self.contentWidget)
        layout.setContentsMargins(10,0,10,0)
        layout.setSpacing(10)

        self.container = QStackedWidget()
        self.container.addWidget(self.emptyStateWidget)
        self.container.addWidget(self.contentWidget)
        self.setWidget(self.container)
        self._cachedItemCount = 0


    def loadTransactions(self, datas : list[Transaction]):
        self.clearTransactions()
        if datas is None or len(datas) == 0:
            return

        for data in datas:
            self.addTransaction(data)
    

    def addTransaction(self, data : Transaction):
        widget = self._createTransactionItem(data)
        widget.setFixedHeight(60)
        widget.setFixedWidth(self.contentWidget.width()-40)
        widget.setParent(self.contentWidget)
        self.contentWidget.layout().addWidget(widget)
        self.contentWidget.setFixedHeight((self._cachedItemCount+1)*70 + 20)
        self._cachedItemCount += 1

        if self.container.currentWidget() != self.contentWidget:
            self.container.setCurrentWidget(self.contentWidget)
        
    
    def clearTransactions(self):
        for item in self.contentWidget.findChildren(QWidget, "transactionItem"):
            item.setParent(None)
            item.deleteLater()
        self.contentWidget.setFixedHeight(0)
        self._cachedItemCount = 0

        if self.container.currentWidget() != self.emptyStateWidget:
            self.container.setCurrentWidget(self.emptyStateWidget)


    def _createTransactionItem(self, data : Transaction):
        widget = QWidget()
        widget.setObjectName("transactionItem")
        widget.mousePressEvent = lambda event, d = data: self.onTransactionItemClicked(d)
        widget.setStyleSheet("""
            #transactionItem {
                background: white;
            }
            """)
        layout = QHBoxLayout(widget)

        from utils.transaction_style import getIconForCategory, getSubColorForCategory, getColorForType
        iconPixmap = QPixmap(getIconForCategory(data.category))
        iconLb = QLabel()
        iconLb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        iconLb.setPixmap(iconPixmap.scaled(28,28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        iconLb.setStyleSheet(f"background: {getSubColorForCategory(data.category)}; border-radius: 5px; padding: 0px 8px 0px 8px; margin-right:10px")

        categoryLb = QLabel()
        categoryLb.setTextFormat(Qt.TextFormat.RichText)
        categoryLb.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        categoryLb.setText(f"<b style='color: black'>{data.note}</b><br><span style='color: gray'>{data.category}</span>")

        amountLb = QLabel()
        amountLb.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        amountLb.setTextFormat(Qt.TextFormat.RichText)
        amountLb.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        amountLb.setText(f"""
                         <span style='color: {getColorForType(data.type)}'>{'+' if data.isIncomeTransaction() else '-'}{data.amount:,.0f} ₫</span>
                         <br><span style='color: gray'>{data.date}</span>""")

        layout.addWidget(iconLb)
        layout.addWidget(categoryLb)
        layout.addSpacing(20)
        layout.addStretch()
        layout.addWidget(amountLb)

        
        return widget
    

    def resizeEvent(self, arg__1):
        super().resizeEvent(arg__1)
        self.contentWidget.setFixedWidth(self.width())
        self.emptyStateWidget.setFixedHeight(self.height() - 20)
        self.emptyStateWidget.setFixedWidth(self.width())
        for item in self.contentWidget.findChildren(QWidget, "transactionItem"):
            item.setFixedWidth(self.contentWidget.width()-40)
            

    def onTransactionItemClicked(self, transaction: Transaction):
        pass