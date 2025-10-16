from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QSizePolicy, QHBoxLayout, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from datetime import datetime

from core.transaction_manager import TransactionManager
from ui.widgets.transaction_viewer import TransactionViewer
from ui.widgets.date_picker import DatePicker
from utils.window_helper import applyDropShadow, installWindowDragging, repolish
from utils.value_formatter import isValidDateString

class TransactionFinder(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.transactionManager : TransactionManager = QApplication.instance().getTransactionManager()
        self.setupUi()
        
    
    def setupUi(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowTitle("Tìm giao dịch")
        self.setStyleSheet("""
            #container {
                background: white;
                border-radius: 8px;
            }
                           
            #titleLb {
                color: black;
            }
                           
            QLineEdit {
                border: 1px solid lightgray;
                border-radius: 5px;
                background: white;
                color: black;
            }
                           
            QLineEdit:focus {
                border: 1px solid #0AB6D1;
            }
                           
            QLineEdit[warning="true"] {
                border: 1px solid red;
            }
            
            #findBtn {
                background: #0AB6D1;
                color: white;
                border-radius: 5px;
            }
            
            #findBtn:hover {
                background: #0A9EBF;
            }
                           
            #quitBtn {
                background: #5496ff;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
            }
            
            #quitBtn:hover {
                background: #297bff;
            }
        """)
        

        self.container = QWidget(self)
        self.container.setObjectName("container")
        applyDropShadow(self.container, radius=10, color=Qt.GlobalColor.black)
        installWindowDragging(self, self.container)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(10)

        titleLb = QLabel("Tìm giao dịch", self.container)
        titleLb.setObjectName("titleLb")
        titleLb.setAlignment(Qt.AlignmentFlag.AlignLeft)
        titleLb.setFont(QFont("Roboto", 16, QFont.Weight.Medium))

        self.findEdit = QLineEdit()
        self.findEdit.setPlaceholderText("Nhập từ khóa...")
        self.findEdit.setObjectName("findEdit")
        self.findEdit.setClearButtonEnabled(True)
        self.findEdit.setFixedHeight(50)
        self.findEdit.setFont(QFont("Roboto", 11))
        searchPixmap = QPixmap(":/resources/images/search.png").scaled(25,25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.findEdit.addAction(searchPixmap, QLineEdit.ActionPosition.LeadingPosition)

        dateLayout = QHBoxLayout()
        dateLayout.setContentsMargins(0,0,0,0)
        dateLayout.setSpacing(10)
        self.startDateEdit = QLineEdit()
        self.startDateEdit.setPlaceholderText("Từ ngày (dd/mm/yyyy)")
        self.startDateEdit.setObjectName("startDateEdit")
        self.startDateEdit.setFixedHeight(50)
        self.startDateEdit.setFont(QFont("Roboto", 11))
        calendarPixmap = QPixmap(":/resources/images/gray_calendar.png").scaled(25,25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        action = self.startDateEdit.addAction(calendarPixmap, QLineEdit.ActionPosition.LeadingPosition)
        action.triggered.connect(self.onStartDateAction)

        self.endDateEdit = QLineEdit()
        self.endDateEdit.setPlaceholderText("Đến ngày (dd/mm/yyyy)")
        self.endDateEdit.setObjectName("endDateEdit")
        self.endDateEdit.setFixedHeight(50)
        self.endDateEdit.setFont(QFont("Roboto", 11))
        action = self.endDateEdit.addAction(calendarPixmap, QLineEdit.ActionPosition.LeadingPosition)
        action.triggered.connect(self.onEndDateAction)

        dateLayout.addWidget(self.startDateEdit)
        dateLayout.addWidget(self.endDateEdit)

        findBtn = QPushButton("Tìm kiếm")
        findBtn.setObjectName("findBtn")
        findBtn.setFixedHeight(40)
        findBtn.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        findBtn.setFlat(True)
        findBtn.clicked.connect(self.onFindClicked)

        self.transactionViewer = TransactionViewer()
        self.transactionViewer.setObjectName("transactionViewer")
        self.transactionViewer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.transactionViewer.setCustomEmptyText("Không tìm thấy giao dịch nào")
        
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0,0,0,0)
        closeBtn = QPushButton("Đóng")
        closeBtn.setObjectName("quitBtn")
        closeBtn.setFixedHeight(40)
        closeBtn.setFont(QFont("Roboto", 11, QFont.Weight.Bold))
        closeBtn.setFlat(True)
        closeBtn.clicked.connect(self.close)

        controlLayout.addStretch()
        controlLayout.addWidget(closeBtn)

        layout.addWidget(titleLb)
        layout.addSpacing(30)
        layout.addWidget(self.findEdit)
        layout.addLayout(dateLayout)
        layout.addWidget(findBtn)
        layout.addSpacing(20)
        layout.addWidget(self.transactionViewer)
        layout.addLayout(controlLayout)

        self.setMinimumSize(600, 800)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.container.setGeometry(10, 10, self.width()-20, self.height()-20)
        
    def onFindClicked(self):
        keyword = self.findEdit.text().strip()
        if keyword == "":
            self.findEdit.setProperty("warning", True)
            self.findEdit.setFocus()
            repolish(self.findEdit)
            return
        else:
            self.findEdit.setProperty("warning", False)
            repolish(self.findEdit)
        
        startDate = self.startDateEdit.text().strip()
        if startDate != "" and not isValidDateString(startDate):
            self.startDateEdit.setProperty("warning", True)
            self.startDateEdit.setFocus()
            self.startDateEdit.setText("")
            repolish(self.startDateEdit)
            return
        else:
            startDate = datetime.strptime(startDate, "%d/%m/%Y").date() if startDate != "" else None
            self.startDateEdit.setProperty("warning", False)
            repolish(self.startDateEdit)
        
        endDate = self.endDateEdit.text().strip()
        if endDate != "" and not isValidDateString(endDate):
            self.endDateEdit.setProperty("warning", True)
            self.endDateEdit.setFocus()
            self.endDateEdit.setText("")
            repolish(self.endDateEdit)
            return
        else:
            endDate = datetime.strptime(endDate, "%d/%m/%Y").date() if endDate != "" else None
            self.endDateEdit.setProperty("warning", False)
            repolish(self.endDateEdit)
        
        results = self.transactionManager.getTransactions(keyword=keyword, startDate=startDate, endDate=endDate)
        self.transactionViewer.loadTransactions(results)

    def onStartDateAction(self):
        endDate = self.endDateEdit.text().strip()
        if endDate == "" or not isValidDateString(endDate):
            endDate = None
        else:
            endDate = datetime.strptime(endDate, "%d/%m/%Y").date()
        dialog = DatePicker(self, lowerDate=None, upperDate=endDate)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.startDateEdit.setText(dialog.getSelectedDate().strftime("%d/%m/%Y"))

    def onEndDateAction(self):
        startDate = self.startDateEdit.text().strip()
        if startDate == "" or not isValidDateString(startDate):
            startDate = None
        else:
            startDate = datetime.strptime(startDate, "%d/%m/%Y").date()
        dialog = DatePicker(self, lowerDate=startDate, upperDate=None)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.endDateEdit.setText(dialog.getSelectedDate().strftime("%d/%m/%Y"))

    