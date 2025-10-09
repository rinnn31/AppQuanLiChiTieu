from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from ui.widgets.transaction_viewer import TransactionViewer
from core.transaction_manager import TransactionManager
from utils.window_helper import applyDropShadow, installWindowDragging

class TransactionFinder(QDialog):
    def __init__(self, transactionManager : TransactionManager,  parent=None):
        super().__init__(parent)
        self._transactionManager = transactionManager
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
                           
            #findEdit {
                border: 1px solid lightgray;
                border-radius: 5px;
                padding: 5px 10px;
                background: white;
                color: black;
            }
                           
            #findEdit:focus {
                border: 1px solid #0AB6D1;
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
        self.findEdit.addAction(QIcon(":/resources/images/search.png"), QLineEdit.ActionPosition.LeadingPosition)

        findBtn = QPushButton("Tìm kiếm")
        findBtn.setObjectName("findBtn")
        findBtn.setFixedHeight(40)
        findBtn.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        findBtn.setFlat(True)
        findBtn.clicked.connect(self.onFindClicked)

        self.transactionViewer = TransactionViewer()
        self.transactionViewer.setObjectName("transactionViewer")
        self.transactionViewer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

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
            return
        results = self._transactionManager.getTransactions(keyword=keyword)
        self.transactionViewer.loadTransactions(results)