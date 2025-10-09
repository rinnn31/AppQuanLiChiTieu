from PySide6.QtWidgets import (QWidget, QDialog, QVBoxLayout, QLabel, QLineEdit, QGridLayout, \
                               QSizePolicy, QSpacerItem, QHBoxLayout, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap

from core.transaction import Transaction
from utils.window_helper import applyDropShadow, repolish, installWindowDragging
from utils.transaction_style import EXPENSE_CATEGORIES, INCOME_CATEGORIES, getIconForCategory, getSubColorForCategory

class TransactionEditor(QDialog):
    def __init__(self, parent: QWidget = None, transaction: Transaction = None, transactionType = 0, editMode: bool = True):
        super().__init__(parent)
        self._transaction = Transaction(transaction.id, transaction.amount, transaction.date, \
                                        transaction.category, transaction.note, transaction.type) \
                                     if transaction else Transaction()
        self._editMode = editMode
        self._transactionType = transactionType
        self.setupUi()


    def setupUi(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("""
            #container {
                background: white;
                border-radius: 10px;
            }
            
            #sectionLb {
                color: #424242;
            }
                           
            QLineEdit {
                background: white;
                border: 2px solid lightgray;
                border-radius: 5px;
                padding: 5px 10px;
                color: black;
            }
            #categoriesWidget {
                background: #f3f5f2;
                border-radius: 5px;
            }

            #categoryItem {
                border-radius: 5px;
            }

            #categoryItem[selected="true"] {
                background: white;
                border: 1px solid rgb(10, 182, 209);
            }
                               
            QLineEdit:focus {
                border: 1px solid rgb(10, 182, 209);
            }   
            #categoryIconLb {
               background: lightgray;
            }         
            #confirmBtn {
                background: #5496ff;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
            }
                           
            #confirmBtn:hover {
                background: #2979ff;
            }
                           
            #cancelBtn, #closeBtn {
                padding: 5px 15px;
                background: white;
                color: black;
            }
        """)
        

        self.container = QWidget(self)
        self.container.setObjectName("container")

        applyDropShadow(self.container, radius=10, color=Qt.GlobalColor.black)
        installWindowDragging(self, self.container)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(5)

        titleLb = QLabel()
        if self._transaction is None:
            titleLb.setText("Thêm khoản thu mới" if self._transactionType == 0 else "Thêm khoản chi mới")
        else:
            titleLb.setText("Chỉnh sửa giao dịch" if self._editMode else "Xem giao dịch")
        titleLb.setObjectName("titleLb")
        titleLb.setFont(QFont("Roboto", 14, QFont.Weight.Medium))
        titleLb.setAlignment(Qt.AlignmentFlag.AlignLeft)
        titleLb.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        def createSectionLabel(text):
            lb = QLabel(text)
            lb.setObjectName("sectionLb")
            lb.setAlignment(Qt.AlignmentFlag.AlignLeft)
            lb.setFont(QFont("Roboto", 11))
            lb.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            applyDropShadow(lb, radius=2)
            return lb

        def createInputField(objectName, placeholder):
            edit = QLineEdit()
            edit.setObjectName(objectName)
            edit.setPlaceholderText(placeholder)
            edit.setFont(QFont("Roboto", 11))
            edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
            edit.setReadOnly(not self._editMode)
            edit.setFixedHeight(45)
            return edit
        
        amountLb = createSectionLabel("Số tiền:")
        self._amountEdit = createInputField("amountEdit", "Nhập số tiền...")
        self._amountEdit.textEdited.connect(self.onAmountTextEdited)

        dateLb = createSectionLabel("Ngày:")
        self._dateEdit = createInputField("dateEdit", "Chọn ngày...")

        categoryLb = createSectionLabel("Danh mục:")

        categoriesWidget = QWidget()
        categoriesWidget.setObjectName("categoriesWidget")
        categoriesWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        categoriesGridLayout = QGridLayout(categoriesWidget)
        categoriesGridLayout.setContentsMargins(10, 10, 10, 10)
        categoriesGridLayout.setSpacing(10)
        categories = INCOME_CATEGORIES if self._transactionType == 0 else EXPENSE_CATEGORIES
        for i, category in enumerate(categories):
            categoryWidget = QWidget()
            categoryWidget.setObjectName("categoryItem")
            categoryWidget.setProperty("selected", False)
            categoryWidget.setProperty("category", category)
            categoryWidget.setFixedSize(80, 80)
            categoryWidget.mousePressEvent = lambda event, c = category: self._onCategoryClicked(c)
            categoryWidget.setCursor(Qt.CursorShape.PointingHandCursor)

            categoryLayout = QVBoxLayout(categoryWidget)
            categoryLayout.setSpacing(5)

            categoryIconLb = QLabel()
            categoryIconLb.setObjectName("categoryIconLb")
            categoryIconLb.setFixedSize(40, 40)
            categoryIconLb.setPixmap(QPixmap(getIconForCategory(category)).scaled(30,30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            categoryIconLb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            categoryIconLb.setStyleSheet(f"background: {getSubColorForCategory(category)}; border-radius: 5px; padding: 5px;")
            categoryIconLb.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

            categoryNameLb = QLabel(category)
            categoryNameLb.setObjectName("categoryNameLb")
            categoryNameLb.setFont(QFont("Roboto", 10))
            categoryNameLb.setAlignment(Qt.AlignmentFlag.AlignCenter)

            categoryLayout.addWidget(categoryIconLb)
            categoryLayout.addWidget(categoryNameLb)

            categoriesGridLayout.addWidget(categoryWidget, i // 4, i % 4)
        
        noteLb = createSectionLabel("Ghi chú:")
        self._noteEdit = createInputField("noteEdit", "Nhập ghi chú...")

        self._warningLb = QLabel("")
        self._warningLb.setObjectName("warningLb")
        self._warningLb.setFont(QFont("Roboto", 10))
        self._warningLb.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._warningLb.setStyleSheet("color: red")
        self._warningLb.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        controlLayout = QHBoxLayout()
        controlSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        controlLayout.addItem(controlSpacer)
        if self._editMode:
            self._confirmBtn = QPushButton("Xác nhận")
            self._confirmBtn.setObjectName("confirmBtn")
            self._confirmBtn.setFont(QFont("Roboto", 11, QFont.Weight.Bold))
            self._confirmBtn.setCursor(Qt.CursorShape.PointingHandCursor)
            self._confirmBtn.setFixedHeight(40)
            self._confirmBtn.setFlat(True)
            self._confirmBtn.clicked.connect(self.onConfirmClicked) 

            self._cancelBtn = QPushButton("Hủy")
            self._cancelBtn.setObjectName("cancelBtn")
            self._cancelBtn.setFont(QFont("Roboto", 11, QFont.Weight.Bold))
            self._cancelBtn.setCursor(Qt.CursorShape.PointingHandCursor)
            self._cancelBtn.setFixedHeight(40)
            self._cancelBtn.setFlat(True)
            self._cancelBtn.clicked.connect(lambda: self.reject())

            controlLayout.addWidget(self._cancelBtn)
            controlLayout.addWidget(self._confirmBtn)
        else:
            self._closeBtn = QPushButton("Đóng")
            self._closeBtn.setObjectName("closeBtn")
            self._closeBtn.setFont(QFont("Roboto", 11, QFont.Weight.Bold))
            self._closeBtn.setCursor(Qt.CursorShape.PointingHandCursor)
            self._closeBtn.setFixedHeight(40)
            self._closeBtn.setFlat(True)
            self._closeBtn.clicked.connect(lambda: self.close())
            controlLayout.addWidget(self._closeBtn)


        layout.addWidget(titleLb)
        layout.addSpacing(25)
        layout.addWidget(amountLb)
        layout.addWidget(self._amountEdit)
        layout.addSpacing(15)
        layout.addWidget(dateLb)
        layout.addWidget(self._dateEdit)
        layout.addSpacing(15)
        layout.addWidget(categoryLb)
        layout.addWidget(categoriesWidget)
        layout.addSpacing(15)
        layout.addWidget(noteLb)
        layout.addWidget(self._noteEdit)
        layout.addSpacing(15)
        layout.addWidget(self._warningLb)
        layout.addSpacing(10)
        layout.addLayout(controlLayout)
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        self.setMinimumSize(430, 670)

    def resizeEvent(self, arg__1):
        super().resizeEvent(arg__1)
        self.container.setGeometry(10, 10, self.width() - 20, self.height() - 20)

    def _onCategoryClicked(self, category):
        if not self._editMode:
            return;
        categoryItems = self.container.findChildren(QWidget, "categoryItem")
        for item in categoryItems:
            item.setProperty("selected", item.property("category") == category)
            repolish(item)

        self._transaction.category = category

    def onAmountTextEdited(self, text):
        if text == "":
            return
        numberStr = ''.join(filter(str.isdigit, text))
        if numberStr == "":
            self._amountEdit.setText("")
            return
        
        number = int(numberStr)
        self._amountEdit.setText(f"{number:,}")

    def onConfirmClicked(self):
        self._warningLb.setText("")
        if self._amountEdit.text() == "":
            self._warningLb.setText("Vui lòng nhập số tiền!")
            return
        if int(self._amountEdit.text().replace(",", "")) >= 1_000_000_000_000:
            self._warningLb.setText("Số tiền không được vượt quá 1,000,000,000,000!")
            return
        if self._transaction.category == "":
            self._warningLb.setText("Vui lòng chọn danh mục!")
            return
        if self._dateEdit.text() == "":
            self._warningLb.setText("Vui lòng chọn ngày!")
            return
        
        self._transaction.amount = int(self._amountEdit.text().replace(",", ""))
        self._transaction.note = self._noteEdit.text()
        self._transaction.type = self._transactionType
        self._transaction.date = self._dateEdit.text()

        self.accept()




