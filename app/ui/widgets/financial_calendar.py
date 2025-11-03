from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, \
                        QLabel, QSizePolicy, QPushButton, QSpacerItem, QDialog, QApplication
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QDate
from datetime import date
from app.database import TransactionManager
from app.utils.window_helper import repolish, applyDropShadow

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
        
        self.containerLayout  = QVBoxLayout(self.container)
        self.containerLayout.setContentsMargins(10,10,10,10)
        self.containerLayout.setSpacing(10)

        self.yearPickerLayout = QHBoxLayout()
        self.yearPickerLayout.setContentsMargins(0,0,0,0)
        self.yearPickerLayout.setSpacing(10)

        self.prevBtn = QPushButton("")
        self.prevBtn.setIcon(QIcon(":/resources/images/black_left_arrow.png"))
        self.prevBtn.setFixedSize(30,30)
        self.prevBtn.setFlat(True)
        self.prevBtn.setObjectName("year_picker_nav_btn")
        self.prevBtn.clicked.connect(self.onPrevYearClicked)

        self.nextBtn = QPushButton("")
        self.nextBtn.setIcon(QIcon(":/resources/images/black_right_arrow.png"))
        self.nextBtn.setFixedSize(30,30)
        self.nextBtn.setFlat(True)
        self.nextBtn.setObjectName("year_picker_nav_btn")
        self.nextBtn.clicked.connect(self.onNextYearClicked)

        self.yearLb = QLabel("2025")
        self.yearLb.setAlignment(Qt.AlignCenter)
        self.yearLb.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.yearLb.setStyleSheet("color: #5c5b5b;")
        self.yearLb.setObjectName("year_picker_lb")
        self.yearLb.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.yearPickerLayout.addWidget(self.prevBtn)
        self.yearPickerLayout.addStretch()
        self.yearPickerLayout.addWidget(self.yearLb)
        self.yearPickerLayout.addStretch()
        self.yearPickerLayout.addWidget(self.nextBtn)

        self.monthsGridLayout = QGridLayout()
        self.monthsGridLayout.setContentsMargins(0,0,0,0)
        self.monthsGridLayout.setSpacing(20)

        for i in range(1, 13):
            monthBtn = QPushButton(f"Tháng {i}")
            monthBtn.setObjectName("month_btn")
            monthBtn.setProperty("selected", "false")
            monthBtn.setFlat(True)
            monthBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            monthBtn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
            monthBtn.setCursor(Qt.PointingHandCursor)
            monthBtn.clicked.connect(lambda checked, m=i: self.onMonthBtnClicked(m))
            self.monthsGridLayout.addWidget(monthBtn, (i-1)//4, (i-1)%4)
        
        self.controlBtnLayout = QHBoxLayout()
        self.controlBtnLayout.setContentsMargins(0,0,0,0)
        self.controlBtnLayout.setSpacing(10)
        self.acceptBtn = QPushButton("OK")
        self.acceptBtn.setObjectName("ok_btn")
        self.acceptBtn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.acceptBtn.setContentsMargins(20,10,20,10)
        self.acceptBtn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.acceptBtn.setFlat(True)
        self.acceptBtn.setCursor(Qt.PointingHandCursor)
        self.acceptBtn.clicked.connect(lambda: self.accept())

        self.cancelBtn = QPushButton("Hủy")
        self.cancelBtn.setObjectName("cancel_btn")
        self.cancelBtn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.cancelBtn.setContentsMargins(20,10,20,10)
        self.cancelBtn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.cancelBtn.setFlat(True)
        self.cancelBtn.setCursor(Qt.PointingHandCursor)
        self.cancelBtn.clicked.connect(lambda: self.reject())

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.controlBtnLayout.addItem(spacer)
        self.controlBtnLayout.addWidget(self.cancelBtn)
        self.controlBtnLayout.addWidget(self.acceptBtn)

        self.containerLayout.addLayout(self.yearPickerLayout)
        self.containerLayout.addLayout(self.monthsGridLayout)
        self.containerLayout.addLayout(self.controlBtnLayout)

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

        self.yearLb.setText(str(self._selectedYear))
        self.prevBtn.setEnabled(self._selectedYear > 2000)
        self.nextBtn.setEnabled(self._selectedYear < QDate.currentDate().year())

        months = self.container.findChildren(QPushButton, "month_btn")
        for i, monthBtn in enumerate(months, 1):
            monthBtn.setProperty("selected", "true" if i == self._selectedMonth else "false")
            if i > QDate.currentDate().month() and self._selectedYear == QDate.currentDate().year():
                monthBtn.setEnabled(False)
            repolish(monthBtn)

    def getSelectedYearMonth(self):
        return self._selectedYear, self._selectedMonth

class FinancialCalendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

        self._selectedDateItem = None
        self.transactionManager = QApplication.instance().getTransactionManager()
        self._currentDate = QDate.currentDate()
        self.updateCalendar()
        
    def setTransactionManager(self, transactionManager: TransactionManager):
        self.transactionManager = transactionManager
    
    def setupUi(self):
        self.setStyleSheet("""
            #calendarNavBtn {
                background: white;
                border-radius: 8px;
            }
            #calendarNavBtn:hover {
                background: #f0f0f0;
            }
            #calendarNavBtn:pressed {
                background: #e0e0e0;
            }
                           
            #calendarDayLb {
                margin-bottom: 20px;
            }
                           
            #calendarDateItem {
                border: 1px solid #e0e0e0;
            }
                           
            #calendarDateItem[selected="true"] {
                background: #d0eaff;
            }
                           
            #calendarDateItem[selected="true"] > QLabel {
                font-weight: bold;
                color: #0047b3;
            }
                           
            #calendarDateLb {
                margin-left: 10px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(20)

        self.monthYearPanel = QWidget()
        self.monthYearPanel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.monthYearPanel.setMinimumHeight(40)
        self.monthYearPanel.setMaximumHeight(60)
        monthYearPanelLayout = QHBoxLayout(self.monthYearPanel)
        monthYearPanelLayout.setContentsMargins(10,10,10,10)
        monthYearPanelLayout.setSpacing(10)

        self.prevBtn = QPushButton("")
        self.prevBtn.setIcon(QIcon(":/resources/images/black_left_arrow.png"))
        self.prevBtn.setFixedSize(40,40)
        self.prevBtn.setObjectName("calendarNavBtn")
        self.prevBtn.clicked.connect(self.onPrevMonthClicked)

        self.nextBtn = QPushButton("")
        self.nextBtn.setIcon(QIcon(":/resources/images/black_right_arrow.png"))
        self.nextBtn.setFixedSize(40,40)
        self.nextBtn.setObjectName("calendarNavBtn")
        self.nextBtn.clicked.connect(self.onNextMonthClicked)

        self.monthYearLb = QLabel("Tháng 1, 2025")
        self.monthYearLb.setAlignment(Qt.AlignCenter)
        self.monthYearLb.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.monthYearLb.setStyleSheet("color: #5c5b5b;")
        self.monthYearLb.setObjectName("calendarMonthYearLb")
        self.monthYearLb.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.monthYearLb.setCursor(Qt.PointingHandCursor)
        self.monthYearLb.mousePressEvent = lambda event: self.onMonthYearClicked()

        monthYearPanelLayout.addWidget(self.prevBtn)
        monthYearPanelLayout.addWidget(self.monthYearLb)
        monthYearPanelLayout.addWidget(self.nextBtn)

        self.calendarGrid = QWidget()
        gridLayout = QGridLayout(self.calendarGrid)
        gridLayout.setContentsMargins(10,0,10,10)
        gridLayout.setSpacing(0)
        for i, day in enumerate(["T2", "T3", "T4", "T5", "T6", "T7", "CN"]):
            dayLb = QLabel(day)
            dayLb.setAlignment(Qt.AlignCenter)
            dayLb.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            dayLb.setObjectName("calendarDayLb")
            gridLayout.addWidget(dayLb, 0, i)
        
        for row in range(1, 6):
            for col in range(7):
                dateWidget = QWidget()
                dateWidget.setObjectName("calendarDateItem")
                dateWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                dateWidget.mousePressEvent = lambda event, w=dateWidget: self._onDateItemSelected(w)
                dateLayout = QVBoxLayout(dateWidget)
                dateLayout.setContentsMargins(5,5,5,5)
                dateLayout.setSpacing(2)

                dateLb = QLabel("11")
                dateLb.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                dateLb.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
                dateLb.setObjectName("calendarDateLb")
                dateLb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

                dateLayout.addWidget(dateLb)
                gridLayout.addWidget(dateWidget, row, col)
        
        layout.addWidget(self.monthYearPanel)
        layout.addWidget(self.calendarGrid)

    def onPrevMonthClicked(self):
        self._currentDate = self._currentDate.addMonths(-1)
        self.updateCalendar()

    def onNextMonthClicked(self):
        self._currentDate = self._currentDate.addMonths(1)
        self.updateCalendar()

    def onMonthYearClicked(self):
        monthYearPicker = MonthYearPicker(self, self._currentDate.year(), self._currentDate.month())
        if monthYearPicker.exec() == QDialog.DialogCode.Accepted:
            selectedYear, selectedMonth = monthYearPicker.getSelectedYearMonth()
            self._currentDate = QDate(selectedYear, selectedMonth, 1)
            self.updateCalendar()

    def _fillCalendar(self):
        self.monthYearLb.setText(self._currentDate.toString("Tháng M, yyyy"))

        firstDayOfMonth = QDate(self._currentDate.year(), self._currentDate.month(), 1)
        startDayOfWeek = firstDayOfMonth.dayOfWeek()
        startDate = firstDayOfMonth.addDays(- (startDayOfWeek - 1) )

        if self.transactionManager:
            datas = self.transactionManager.getDailyTotalsInPeriod(firstDayOfMonth.toPython(), min(firstDayOfMonth.addMonths(1).addDays(-1).toPython(), QDate.currentDate().toPython()))
        else:
            datas = {}

        gridLayout : QGridLayout = self.calendarGrid.layout()
        for row in range(1, 6):
            for col in range(7):
                dateWidget = gridLayout.itemAtPosition(row, col).widget()
                dateLb = dateWidget.findChild(QLabel, "calendarDateLb")
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
                    from app.utils.value_formatter import getShortMoneyString
                    income, expense = datas[date.toString("yyyy-MM-dd")]
                    if income > 0:
                        incomeLb = QLabel(getShortMoneyString(income, ""), parent=dateWidget)
                        incomeLb.setObjectName("incomeLb")
                        incomeLb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                        incomeLb.setFont(QFont("Segoe UI", 11))
                        incomeLb.setStyleSheet("color: #18973A;")
                        incomeLb.setAlignment(Qt.AlignmentFlag.AlignRight)
                        dateWidget.layout().addWidget(incomeLb)
                    if expense > 0:
                        expenseLb = QLabel(getShortMoneyString(expense, ""), parent=dateWidget)
                        expenseLb.setObjectName("expenseLb")
                        expenseLb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                        expenseLb.setFont(QFont("Segoe UI", 11))
                        expenseLb.setStyleSheet("color: #D91F1F;")
                        expenseLb.setAlignment(Qt.AlignmentFlag.AlignRight)
                        dateWidget.layout().addWidget(expenseLb)

        self._onDateItemSelected(None)

    def updateCalendar(self):
        self.prevBtn.setEnabled(not (self._currentDate.year() == 2000 and self._currentDate.month() == 1))
        self.nextBtn.setEnabled(not (self._currentDate.year() == QDate.currentDate().year() and self._currentDate.month() == QDate.currentDate().month()))
        self._fillCalendar()

    def _onDateItemSelected(self, selectedItem: QWidget):
        from app.utils.window_helper import repolish
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
        
        