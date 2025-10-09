from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, \
                        QLabel, QSizePolicy, QPushButton, QSpacerItem, QDialog, QSlider
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QDate
from datetime import date
from core.transaction_manager import TransactionManager
from utils.window_helper import repolish, applyDropShadow

class MonthYearPicker(QDialog):
    def __init__(self, parent=None, initialYear=2025, initialMonth=1):
        super().__init__(parent)
        self.setupUi()
        self._selectedYear = initialYear
        self._selectedMonth = initialMonth
        self._update()

    def setupUi(self):
        
        self.setStyleSheet("""
            #month_year_picker_container {
                background: white;
                border-radius: 10px;
            }   

            #year_picker_nav_btn {
                background: white;
                border-radius: 8px;
            }
                           
            #year_picker_nav_btn:hover {
                background: #f0f0f0;
            }
                           
            #year_picker_nav_btn:pressed {
                background: #e0e0e0
            }   
                           
            QGridLayout {
                margin-top: 20px;
                margin-bottom: 10px;
            }
                           
            #month_btn {
                background: white;
                border-radius: 8px;
                color: black;
            }

            #month_btn[enabled="false"] {
                color: gray;
            } 
            #month_btn:hover {
                background: #f0f0f0;
            }
                           
            #month_btn[selected="true"] {
                background: #d0eaff;
            }   

            #ok_btn, #cancel_btn {
                background: white;
                border-radius: 8px;
                padding: 5px 15px;
            }
                        
                           
            #ok_btn {
                color: #108a03;
            }
                           
            #cancel_btn {
                color: #ba0000;
            }
                           
            #ok_btn:hover, #cancel_btn:hover {
                background: #f0f0f0;
            }

            #ok_btn:pressed, #cancel_btn:pressed {
                background: #e0e0e0;
            }           
            
        
        """)
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.container = QWidget(self)
        self.container.setObjectName("month_year_picker_container")
        applyDropShadow(self.container, radius=10)
        
        layout  = QVBoxLayout(self.container)
        layout.setContentsMargins(10,10,10,10)
        layout.setSpacing(10)

        yearPickerLayout = QHBoxLayout()
        yearPickerLayout.setContentsMargins(0,0,0,0)
        yearPickerLayout.setSpacing(10)

        self._prevBtn = QPushButton("")
        self._prevBtn.setIcon(QIcon(":/resources/images/black_left_arrow.png"))
        self._prevBtn.setFixedSize(30,30)
        self._prevBtn.setFlat(True)
        self._prevBtn.setObjectName("year_picker_nav_btn")
        self._prevBtn.clicked.connect(self.onPrevYearClicked)

        self._nextBtn = QPushButton("")
        self._nextBtn.setIcon(QIcon(":/resources/images/black_right_arrow.png"))
        self._nextBtn.setFixedSize(30,30)
        self._nextBtn.setFlat(True)
        self._nextBtn.setObjectName("year_picker_nav_btn")
        self._nextBtn.clicked.connect(self.onNextYearClicked)

        self._yearLb = QLabel("2025")
        self._yearLb.setAlignment(Qt.AlignCenter)
        self._yearLb.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self._yearLb.setStyleSheet("color: #5c5b5b;")
        self._yearLb.setObjectName("year_picker_lb")
        self._yearLb.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        yearPickerLayout.addWidget(self._prevBtn)
        yearPickerLayout.addWidget(self._yearLb)
        yearPickerLayout.addWidget(self._nextBtn)

        gridLayout = QGridLayout()
        gridLayout.setContentsMargins(0,0,0,0)
        gridLayout.setSpacing(20)

        for i in range(1, 13):
            monthBtn = QPushButton(f"Tháng {i}")
            monthBtn.setObjectName("month_btn")
            monthBtn.setProperty("selected", "false")
            monthBtn.setFlat(True)
            monthBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            monthBtn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
            monthBtn.setCursor(Qt.PointingHandCursor)
            monthBtn.clicked.connect(lambda checked, m=i: self.onMonthBtnClicked(m))
            gridLayout.addWidget(monthBtn, (i-1)//4, (i-1)%4)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(0,0,0,0)
        buttonLayout.setSpacing(10)
        self._okBtn = QPushButton("OK")
        self._okBtn.setObjectName("ok_btn")
        self._okBtn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self._okBtn.setContentsMargins(20,10,20,10)
        self._okBtn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self._okBtn.setFlat(True)
        self._okBtn.setCursor(Qt.PointingHandCursor)
        self._okBtn.clicked.connect(lambda: self.accept())

        self._cancelBtn = QPushButton("Hủy")
        self._cancelBtn.setObjectName("cancel_btn")
        self._cancelBtn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self._cancelBtn.setContentsMargins(20,10,20,10)
        self._cancelBtn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self._cancelBtn.setFlat(True)
        self._cancelBtn.setCursor(Qt.PointingHandCursor)
        self._cancelBtn.clicked.connect(lambda: self.reject())

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        buttonLayout.addItem(spacer)
        buttonLayout.addWidget(self._cancelBtn)
        buttonLayout.addWidget(self._okBtn)

        layout.addLayout(yearPickerLayout)
        layout.addLayout(gridLayout)
        layout.addLayout(buttonLayout)

    def resizeEvent(self, arg__1):
        super().resizeEvent(arg__1)
        self.container.setGeometry(10,10,self.width()-20,self.height()-20)

    def onNextYearClicked(self):
        self._selectedYear += 1
        self._update()

    def onPrevYearClicked(self):
        self._selectedYear -= 1
        self._update()

    def onMonthBtnClicked(self, month):
        self._selectedMonth = month
        self._update()

    def _update(self):
        self._selectedYear = max(2000, min(self._selectedYear, QDate.currentDate().year()))
        self._selectedMonth = max(1, min(self._selectedMonth, 12))

        self._yearLb.setText(str(self._selectedYear))
        self._prevBtn.setEnabled(self._selectedYear > 2000)
        self._nextBtn.setEnabled(self._selectedYear < QDate.currentDate().year())

        months = self.container.findChildren(QPushButton, "month_btn")
        for i, monthBtn in enumerate(months, 1):
            monthBtn.setProperty("selected", "true" if i == self._selectedMonth else "false")
            if i > QDate.currentDate().month() and self._selectedYear == QDate.currentDate().year():
                monthBtn.setEnabled(False)
            repolish(monthBtn)

    def getSelectedDate(self):
        return self._selectedYear, self._selectedMonth

class FinanceCalendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

        self._selectedDateItem = None
        self._transactionManager = None
        self._currentDate = QDate.currentDate()
        self.updateCalendar()
        
    def setTransactionManager(self, transactionManager: TransactionManager):
        self._transactionManager = transactionManager
    
    def setupUi(self):
        self.setStyleSheet("""
            #calendar_nav_btn {
                background: white;
                border-radius: 8px;
            }
            #calendar_nav_btn:hover {
                background: #f0f0f0;
            }
            #calendar_nav_btn:pressed {
                background: #e0e0e0;
            }
                           
            #calendar_day_lb {
                margin-bottom: 20px;
            }
                           
            #calendar_date_item {
                border: 1px solid #e0e0e0;
            }
                           
            #calendar_date_item[selected="true"] {
                background: #d0eaff;
            }
                           
            #calendar_date_item[selected="true"] > QLabel {
                font-weight: bold;
                color: #0047b3;
            }
                           
            #calendar_date_lb {
                margin-left: 10px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(20)

        self._panelWidget = QWidget()
        self._panelWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._panelWidget.setMinimumHeight(40)
        self._panelWidget.setMaximumHeight(60)
        panelLayout = QHBoxLayout(self._panelWidget)
        panelLayout.setContentsMargins(10,10,10,10)
        panelLayout.setSpacing(10)

        self._prevBtn = QPushButton("")
        self._prevBtn.setIcon(QIcon(":/resources/images/black_left_arrow.png"))
        self._prevBtn.setFixedSize(40,40)
        self._prevBtn.setObjectName("calendar_nav_btn")
        self._prevBtn.clicked.connect(self.onPrevMonthClicked)

        self._nextBtn = QPushButton("")
        self._nextBtn.setIcon(QIcon(":/resources/images/black_right_arrow.png"))
        self._nextBtn.setFixedSize(40,40)
        self._nextBtn.setObjectName("calendar_nav_btn")
        self._nextBtn.clicked.connect(self.onNextMonthClicked)

        self._monthYearLb = QLabel("Tháng 1, 2025")
        self._monthYearLb.setAlignment(Qt.AlignCenter)
        self._monthYearLb.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self._monthYearLb.setStyleSheet("color: #5c5b5b;")
        self._monthYearLb.setObjectName("calendar_month_year_lb")
        self._monthYearLb.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._monthYearLb.setCursor(Qt.PointingHandCursor)
        self._monthYearLb.mousePressEvent = lambda event: self.onMonthYearClicked()

        panelLayout.addWidget(self._prevBtn)
        panelLayout.addWidget(self._monthYearLb)
        panelLayout.addWidget(self._nextBtn)

        self._calendarGrid = QWidget()
        gridLayout = QGridLayout(self._calendarGrid)
        gridLayout.setContentsMargins(10,0,10,10)
        gridLayout.setSpacing(0)
        for i, day in enumerate(["T2", "T3", "T4", "T5", "T6", "T7", "CN"]):
            dayLb = QLabel(day)
            dayLb.setAlignment(Qt.AlignCenter)
            dayLb.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            dayLb.setObjectName("calendar_day_lb")
            gridLayout.addWidget(dayLb, 0, i)
        
        for row in range(1, 6):
            for col in range(7):
                dateWidget = QWidget()
                dateWidget.setObjectName("calendar_date_item")
                dateWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                dateWidget.mousePressEvent = lambda event, w=dateWidget: self._onDateItemSelected(w)
                dateLayout = QVBoxLayout(dateWidget)
                dateLayout.setContentsMargins(5,5,5,5)
                dateLayout.setSpacing(2)

                dateLb = QLabel("11")
                dateLb.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                dateLb.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
                dateLb.setObjectName("calendar_date_lb")
                dateLb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

                dateLayout.addWidget(dateLb)
                gridLayout.addWidget(dateWidget, row, col)
        
        layout.addWidget(self._panelWidget)
        layout.addWidget(self._calendarGrid)

    def onPrevMonthClicked(self):
        self._currentDate = self._currentDate.addMonths(-1)
        self.updateCalendar()

    def onNextMonthClicked(self):
        self._currentDate = self._currentDate.addMonths(1)
        self.updateCalendar()

    def onMonthYearClicked(self):
        monthYearPicker = MonthYearPicker(self, self._currentDate.year(), self._currentDate.month())
        if monthYearPicker.exec() == QDialog.DialogCode.Accepted:
            selectedYear, selectedMonth = monthYearPicker.getSelectedDate()
            self._currentDate = QDate(selectedYear, selectedMonth, 1)
            self.updateCalendar()

    def _fillCalendar(self):
        self._monthYearLb.setText(self._currentDate.toString("Tháng M, yyyy"))

        firstDayOfMonth = QDate(self._currentDate.year(), self._currentDate.month(), 1)
        startDayOfWeek = firstDayOfMonth.dayOfWeek()
        startDate = firstDayOfMonth.addDays(- (startDayOfWeek - 1) )

        if self._transactionManager:
            datas = self._transactionManager.getDailyTotalsInPeriod(firstDayOfMonth.toPython(), min(firstDayOfMonth.addMonths(1).addDays(-1).toPython(), QDate.currentDate().toPython()))
        else:
            datas = {}

        gridLayout : QGridLayout = self._calendarGrid.layout()
        for row in range(1, 6):
            for col in range(7):
                dateWidget = gridLayout.itemAtPosition(row, col).widget()
                dateLb = dateWidget.findChild(QLabel, "calendar_date_lb")
                date = startDate.addDays((row - 1) * 7 + col)
                dateWidget.setProperty("data", date.toPython())
                dateLb.setText(str(date.day()))
                if date.month() != self._currentDate.month() or date > QDate.currentDate():
                    dateLb.setStyleSheet("color: gray;")
                    dateWidget.setEnabled(False)
                else:
                    dateLb.setStyleSheet("color: black;")
                    dateWidget.setEnabled(True)

                if dateWidget.findChild(QLabel, "incomeLb"):
                    incomeLb = dateWidget.findChild(QLabel, "incomeLb")
                    incomeLb.setParent(None)
                    incomeLb.deleteLater()
                if dateWidget.findChild(QLabel, "expenseLb"):
                    expenseLb = dateWidget.findChild(QLabel, "expenseLb")
                    expenseLb.setParent(None)
                    expenseLb.deleteLater()

                if date.toString("yyyy-MM-dd") in datas:
                    from utils.money_string import getShortMoneyStringInVND
                    income, expense = datas[date.toString("yyyy-MM-dd")]
                    if income > 0:
                        incomeLb = QLabel(getShortMoneyStringInVND(income, ""), parent=dateWidget)
                        incomeLb.setObjectName("incomeLb")
                        incomeLb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                        incomeLb.setFont(QFont("Segoe UI", 10))
                        incomeLb.setStyleSheet("color: #18973A;")
                        incomeLb.setAlignment(Qt.AlignmentFlag.AlignRight)
                        dateWidget.layout().addWidget(incomeLb)
                    if expense > 0:
                        expenseLb = QLabel(getShortMoneyStringInVND(expense, ""), parent=dateWidget)
                        expenseLb.setObjectName("expenseLb")
                        expenseLb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                        expenseLb.setFont(QFont("Segoe UI", 10))
                        expenseLb.setStyleSheet("color: #D91F1F;")
                        expenseLb.setAlignment(Qt.AlignmentFlag.AlignRight)
                        dateWidget.layout().addWidget(expenseLb)

        self._onDateItemSelected(None)

    def updateCalendar(self):
        self._prevBtn.setEnabled(not (self._currentDate.year() == 2000 and self._currentDate.month() == 1))
        self._nextBtn.setEnabled(not (self._currentDate.year() == QDate.currentDate().year() and self._currentDate.month() == QDate.currentDate().month()))
        self._fillCalendar()

    def _onDateItemSelected(self, selectedItem: QWidget):
        from utils.window_helper import repolish
        if self._selectedDateItem:
            self._selectedDateItem.setProperty("selected", "false")
            repolish(self._selectedDateItem)

        if selectedItem and self._selectedDateItem != selectedItem:
            self._selectedDateItem = selectedItem
            selectedItem.setProperty("selected", "true")
            repolish(selectedItem)
            self.onDateSelected(selectedItem.property("data"))
        else:
            self._selectedDateItem = None
            self.onDateSelected(None)


    def onDateSelected(self, date: date):
        ''' Hàm này sẽ được gọi khi người dùng chọn một ngày cụ thể trong lịch.
        '''
        pass
        
        