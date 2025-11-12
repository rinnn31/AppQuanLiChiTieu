from PySide6.QtWidgets import (QWidget, QDialog, QVBoxLayout, QLabel, QLineEdit, QGridLayout, \
                               QSizePolicy, QSpacerItem, QHBoxLayout, QPushButton, QApplication)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QRegularExpressionValidator

from app.database import Transaction
from app.ui.widgets.date_picker import DatePicker
from app.utils.window_helper import applyDropShadow, repolish, installWindowDragging
from app.utils.transaction_style import EXPENSE_CATEGORIES, INCOME_CATEGORIES, getIconForCategory, getSubColorForCategory
from app.utils.value_formatter import isValidDateString, convertDateStringFormat

class TransactionEditor(QDialog):
    def __init__(self, parent: QWidget = None, transactionType = 0, editMode: bool = True, transactionId : int = None):
        super().__init__(parent)
        self._transactionId = transactionId
        self._editMode = editMode
        self._transactionType = transactionType
        self._transactionManager = QApplication.instance().getTransactionManager()
        self.setupUi()
        self._initValue()

    def _initValue(self):
        if self._transactionId is not None:
            transaction = self._transactionManager.getTransactionById(self._transactionId)
            self.onAmountTextEdited(str(transaction.amount))
            self.dateEdit.setText(convertDateStringFormat(transaction.date, currentFormat="%Y-%m-%d", targetFormat="%d/%m/%Y"))
            self.noteEdit.setText(transaction.note)
            self.setCategory(transaction.category)


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
                           
            QLineEdit[warning="true"] {
                border: 2px solid red;
            }
                           
            #categoriesWidget {
                background: #f3f5f2;
                border-radius: 5px;
            }

            #categoryItem {
                border-radius: 5px;
                background: #f3f5f2;
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
                           
            #deleteBtn {
                background: #ff5252;
                color: white;
                border-radius: 5px;
                padding: 5px 20px;
            }
                           
            #deleteBtn:hover {
                background: #ff1744;
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
        

        self._container = QWidget(self)
        self._container.setObjectName("container")
        applyDropShadow(self._container, radius=10, color=Qt.GlobalColor.black)
        installWindowDragging(self, self._container)

        layout = QVBoxLayout(self._container)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(5)

        titleLb = QLabel()
        if self._transactionId is None:
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
            edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus if self._editMode else Qt.FocusPolicy.NoFocus)
            edit.setFixedHeight(45)
            def removeWarning(event, ed=edit):
                ed.setProperty("warning", False)
                repolish(ed)
                QLineEdit.focusInEvent(ed, event)
            edit.focusInEvent = removeWarning
            return edit

        amountLb = createSectionLabel("Số tiền:")
        self.amountEdit = createInputField("amountEdit", "Nhập số tiền...")
        self.amountEdit.textEdited.connect(self.onAmountTextEdited)

        dateLb = createSectionLabel("Ngày:")
        self.dateEdit = createInputField("dateEdit", "Chọn ngày... (01/01/2024)")
        self.dateEdit.setValidator(QRegularExpressionValidator(r"\d{2}/\d{2}/\d{4}")) 
        if self._editMode:
            calendarPixmap = QPixmap(":/resources/images/gray_calendar.png").scaled(20,20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            selectDateAct = self.dateEdit.addAction(calendarPixmap, QLineEdit.ActionPosition.TrailingPosition)
            selectDateAct.triggered.connect(self.onDatePickerTriggered)

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
            if self._editMode:
                categoryWidget.mousePressEvent = lambda event, c = category: self.setCategory(c)
            categoryWidget.setProperty("selected", False)
            categoryWidget.setProperty("category", category)
            categoryWidget.setFixedSize(80, 80)
            categoryWidget.setCursor(Qt.CursorShape.PointingHandCursor)

            categoryLayout = QVBoxLayout(categoryWidget)
            categoryLayout.setSpacing(5)

            categoryIconLb = QLabel()
            categoryIconLb.setObjectName("categoryIconLb")
            categoryIconLb.setFixedHeight(40)
            categoryIconLb.setPixmap(QPixmap(getIconForCategory(category)).scaled(30,30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            categoryIconLb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            categoryIconLb.setStyleSheet(f"background: {getSubColorForCategory(category)}; border-radius: 5px; padding: 5px; margin: 0px 8px;")
            categoryNameLb = QLabel(category)
            categoryNameLb.setObjectName("categoryNameLb")
            categoryNameLb.setStyleSheet("background: transparent;")
            categoryNameLb.setFont(QFont("Roboto", 10))
            categoryNameLb.setAlignment(Qt.AlignmentFlag.AlignCenter)

            categoryLayout.addWidget(categoryIconLb)
            categoryLayout.addWidget(categoryNameLb)

            categoriesGridLayout.addWidget(categoryWidget, i // 4, i % 4)
        
        noteLb = createSectionLabel("Ghi chú:")
        self.noteEdit = createInputField("noteEdit", "Nhập ghi chú...")

        self.warningLb = QLabel("")
        self.warningLb.setObjectName("warningLb")
        self.warningLb.setFont(QFont("Roboto", 10))
        self.warningLb.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.warningLb.setStyleSheet("color: red")
        self.warningLb.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        controlLayout = QHBoxLayout()
        controlSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        controlLayout.addItem(controlSpacer)
        if self._editMode:
            self.confirmBtn = QPushButton("Xác nhận")
            self.confirmBtn.setObjectName("confirmBtn")
            self.confirmBtn.setFont(QFont("Roboto", 11, QFont.Weight.Bold))
            self.confirmBtn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.confirmBtn.setFixedHeight(40)
            self.confirmBtn.setFlat(True)
            self.confirmBtn.clicked.connect(self.onConfirmClicked) 

            if self._transactionId:
                self.deleteBtn = QPushButton("Xóa")
                self.deleteBtn.setObjectName("deleteBtn")
                self.deleteBtn.setFont(QFont("Roboto", 11, QFont.Weight.Bold))
                self.deleteBtn.setCursor(Qt.CursorShape.PointingHandCursor)
                self.deleteBtn.setFixedHeight(40)
                self.deleteBtn.setFlat(True)
                self.deleteBtn.clicked.connect(self.onDeleteClicked)

            self.cancelBtn = QPushButton("Hủy")
            self.cancelBtn.setObjectName("cancelBtn")
            self.cancelBtn.setFont(QFont("Roboto", 11, QFont.Weight.Bold))
            self.cancelBtn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.cancelBtn.setFixedHeight(40)
            self.cancelBtn.setFlat(True)
            self.cancelBtn.clicked.connect(lambda: self.reject())

            controlLayout.addWidget(self.cancelBtn)
            if self._transactionId:
                controlLayout.addWidget(self.deleteBtn)
            controlLayout.addWidget(self.confirmBtn)
        else:
            self.closeBtn = QPushButton("Đóng")
            self.closeBtn.setObjectName("closeBtn")
            self.closeBtn.setFont(QFont("Roboto", 11, QFont.Weight.Bold))
            self.closeBtn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.closeBtn.setFixedHeight(40)
            self.closeBtn.setFlat(True)
            self.closeBtn.clicked.connect(lambda: self.close())
            controlLayout.addWidget(self.closeBtn)

        layout.addWidget(titleLb)
        layout.addSpacing(25)
        layout.addWidget(amountLb)
        layout.addWidget(self.amountEdit)
        layout.addSpacing(15)
        layout.addWidget(dateLb)
        layout.addWidget(self.dateEdit)
        layout.addSpacing(15)
        layout.addWidget(categoryLb)
        layout.addWidget(categoriesWidget)
        layout.addSpacing(15)
        layout.addWidget(noteLb)
        layout.addWidget(self.noteEdit)
        layout.addSpacing(15)
        layout.addWidget(self.warningLb)
        layout.addSpacing(10)
        layout.addLayout(controlLayout)
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        self.setMinimumSize(430, 670)

    def resizeEvent(self, arg__1):
        super().resizeEvent(arg__1)
        self._container.setGeometry(10, 10, self.width() - 20, self.height() - 20)

    def onDeleteClicked(self):
        self._transactionManager.deleteTransaction(self._transactionId)
        self.accept()

    def _getSelectedCategory(self):
        categories = self.findChildren(QWidget, "categoryItem", Qt.FindChildOption.FindChildrenRecursively)
        for category in categories:
            if category.property("selected"):
                return category.property("category")
        return None
    
    def setCategory(self, category):
        categories = self.findChildren(QWidget, "categoryItem", Qt.FindChildOption.FindChildrenRecursively)
        for categoryItem in categories:
            if categoryItem.property("category") == category:
                categoryItem.setProperty("selected", True)
            else:
                categoryItem.setProperty("selected", False)
            repolish(categoryItem)

    def onAmountTextEdited(self, text):
        if text == "":
            return
        numberStr = ''.join(filter(str.isdigit, text))
        if numberStr == "":
            self.amountEdit.setText("")
            return
        
        number = int(numberStr)
        self.amountEdit.setText(f"{number:,}")

    def onConfirmClicked(self):
        # Lấy dữ liệu từ form
        amount = self.amountEdit.text().replace(",", "")
        date = self.dateEdit.text()
        category = self._getSelectedCategory()
        note = self.noteEdit.text()

        self.warningLb.setText("")
        # Kiêm tra tính hợp lệ của dữ liệu, nếu không hợp lệ thì hiển thị cảnh báo
        if amount == "":
            self.warningLb.setText("Vui lòng nhập số tiền!")
            # Chuyển sang trạng thái cảnh báo cho ô nhập liệu, viền đỏ
            self.amountEdit.setProperty("warning", True)
            repolish(self.amountEdit)
            return
        if int(amount) >= 1_000_000_000_000:
            self.warningLb.setText("Số tiền không được vượt quá 1,000,000,000,000!")
            self.amountEdit.setProperty("warning", True)
            repolish(self.amountEdit)
            return
        if date == "":
            self.warningLb.setText("Vui lòng chọn ngày!")
            self.dateEdit.setProperty("warning", True)
            repolish(self.dateEdit)
            return
        if not isValidDateString(date):
            self.warningLb.setText("Ngày không hợp lệ!")
            self.dateEdit.setProperty("warning", True)
            repolish(self.dateEdit)
            return
        if category == "":
            self.warningLb.setText("Vui lòng chọn danh mục!")
            return
        
        formatedDate = convertDateStringFormat(date)
        # Tạo đối tượng Transaction từ dữ liệu nhập vào
        transaction = Transaction(self._transactionId, int(amount), category, self._transactionType, formatedDate, note)
        # Nếu có transactionId thì cập nhật giao dịch, ngược lại thêm giao dịch mới
        if self._transactionId:
            self._transactionManager.updateTransaction(transaction)
        else:
            self._transactionManager.addTransaction(transaction)
        # Đóng hộp thoại và trả về kết quả thành công
        self.accept()

    def onDatePickerTriggered(self):
        datePicker = DatePicker(self)
        if datePicker.exec() == QDialog.DialogCode.Accepted:
            self.dateEdit.setText(datePicker.getSelectedDate().strftime("%d/%m/%Y"))


