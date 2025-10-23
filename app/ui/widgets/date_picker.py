from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QGridLayout, QLabel
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QFont, QIcon
from utils.window_helper import applyDropShadow
from datetime import datetime

class DatePicker(QDialog):
    def __init__(self, parent=None, lowerDate=None, upperDate=None):
        super().__init__(parent)
        self._lowerDate = lowerDate if lowerDate else datetime(2000, 1, 1).date()
        self._upperDate = upperDate if upperDate else datetime.now().date()
        self._currentYear = datetime.now().year
        self._currentMonth = datetime.now().month
        self.setupUI()
        self.updateCalendar()

    def setupUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            #container {
                background: white;
                border-radius: 10px;
            }
            #arrowBtn {
                background: white;
                border: none;
                border-radius: 8px;
            }
            #arrowBtn:hover {
                background: #f0f0f0;
            }
                           
            #dateBtn {
                background: white;
                border: none;
                border-radius: 8px;
                color: black;
            }
                           
            #dateBtn:hover {
                background: #3c81e8;
                color: white;
            }
                           
            #dateBtn:!enabled {
                color: gray;
            }
                           
        """)

        self.container = QWidget(self)
        self.container.setObjectName("container")
        applyDropShadow(self.container, radius=5)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        yearLayout = QHBoxLayout()
        yearLayout.setContentsMargins(10,0,10,0)
        self.prevYearBtn = QPushButton()
        self.prevYearBtn.setObjectName("arrowBtn")
        self.prevYearBtn.setIcon(QIcon(":/resources/images/black_left_arrow.png"))
        self.prevYearBtn.setIconSize(QSize(16, 16))
        self.prevYearBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prevYearBtn.setFlat(True)
        self.prevYearBtn.setFixedSize(24, 24)
        self.prevYearBtn.clicked.connect(self.onPrevYearClicked)

        self.nextYearBtn = QPushButton()
        self.nextYearBtn.setObjectName("arrowBtn")
        self.nextYearBtn.setIcon(QIcon(":/resources/images/black_right_arrow.png"))
        self.nextYearBtn.setIconSize(QSize(16, 16))
        self.nextYearBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.nextYearBtn.setFlat(True)
        self.nextYearBtn.setFixedSize(24, 24)
        self.nextYearBtn.clicked.connect(self.onNextYearClicked)

        self.yearLb = QLabel("2024")
        self.yearLb.mousePressEvent = lambda event: self.accept()  # Placeholder for year selection
        self.yearLb.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
        self.yearLb.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yearLayout.addWidget(self.prevYearBtn)
        yearLayout.addStretch()
        yearLayout.addWidget(self.yearLb)
        yearLayout.addStretch()
        yearLayout.addWidget(self.nextYearBtn)

        monthLayout = QHBoxLayout()
        monthLayout.setContentsMargins(10,0,10,0)
        self.prevMonthBtn = QPushButton()
        self.prevMonthBtn.setObjectName("arrowBtn")
        self.prevMonthBtn.setIcon(QIcon(":/resources/images/black_left_arrow.png"))
        self.prevMonthBtn.setIconSize(QSize(16, 16))
        self.prevMonthBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prevMonthBtn.setFlat(True)
        self.prevMonthBtn.setFixedSize(24, 24)
        self.prevMonthBtn.clicked.connect(self.onPrevMonthClicked)

        self.nextMonthBtn = QPushButton()
        self.nextMonthBtn.setObjectName("arrowBtn")
        self.nextMonthBtn.setIcon(QIcon(":/resources/images/black_right_arrow.png"))
        self.nextMonthBtn.setIconSize(QSize(16, 16))
        self.nextMonthBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.nextMonthBtn.setFlat(True)
        self.nextMonthBtn.setFixedSize(24, 24)
        self.nextMonthBtn.clicked.connect(self.onNextMonthClicked)

        self.monthLb = QLabel("Tháng 6")
        self.monthLb.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
        self.monthLb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        monthLayout.addWidget(self.prevMonthBtn)
        monthLayout.addStretch()
        monthLayout.addWidget(self.monthLb)
        monthLayout.addStretch()
        monthLayout.addWidget(self.nextMonthBtn)
    
        self.dayLayout = QGridLayout()
        self.dayLayout.setSpacing(5)
        days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        for i, day in enumerate(days):
            dayLb = QLabel(day)
            dayLb.setFont(QFont("Roboto", 9, QFont.Weight.Bold))
            dayLb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dayLayout.addWidget(dayLb, 0, i)
        for week in range(1, 6):
            for day in range(7):
                dateBtn = QPushButton(str(week * 7 + day - 6)) 
                dateBtn.setObjectName("dateBtn")
                dateBtn.setFont(QFont("Roboto", 9))
                dateBtn.setCursor(Qt.CursorShape.PointingHandCursor)
                dateBtn.setFlat(True)
                dateBtn.setFixedSize(30, 30)
                dateBtn.clicked.connect(lambda checked, btn=dateBtn: self.onDateButtonClicked(btn))
                self.dayLayout.addWidget(dateBtn, week, day)
        
        layout.addLayout(yearLayout)
        layout.addLayout(monthLayout)
        layout.addLayout(self.dayLayout)

        self.setFixedSize(300, 350)

    def resizeEvent(self, arg__1):
        super().resizeEvent(arg__1)
        self.container.setGeometry(5, 5, self.width()-10, self.height()-10)
    
    def updateCalendar(self):
        if self._currentMonth < 1:
            self._currentMonth = 12
            self._currentYear -= 1
        elif self._currentMonth > 12:
            self._currentMonth = 1
            self._currentYear += 1
        if self._currentYear < self._lowerDate.year or self._currentYear > self._upperDate.year:
            self._currentYear = max(self._lowerDate.year, min(self._currentYear, self._upperDate.year))
            self._currentMonth = max(1, min(self._currentMonth, 12))
        
        self.prevYearBtn.setEnabled(self._currentYear > self._lowerDate.year)
        self.nextYearBtn.setEnabled(self._currentYear < self._upperDate.year)
        self.prevMonthBtn.setEnabled(not (self._currentYear == self._lowerDate.year and self._currentMonth == self._lowerDate.month))
        self.nextMonthBtn.setEnabled(not (self._currentYear == self._upperDate.year and self._currentMonth == self._upperDate.month))

    
        self._fillCalendar()

    def _fillCalendar(self):
        self.yearLb.setText(str(self._currentYear))
        self.monthLb.setText(f"Tháng {self._currentMonth}")

        firstDayOfMonth = QDate(self._currentYear, self._currentMonth, 1)
        startDayOfWeek = firstDayOfMonth.dayOfWeek()
        startDate = firstDayOfMonth.addDays(- (startDayOfWeek - 1) )

        for i in range(1, 6):
            for j in range(7):
                dateBtn = self.dayLayout.itemAtPosition(i, j).widget()
                currentDate = startDate.addDays((i - 1) * 7 + j)
                dateBtn.setText(str(currentDate.day()))
                dateBtn.setEnabled(self._lowerDate <= currentDate.toPython() <= self._upperDate and currentDate.month() == self._currentMonth)

    def onPrevYearClicked(self):
        self._currentYear -= 1
        self.updateCalendar()

    def onNextYearClicked(self):
        self._currentYear += 1
        self.updateCalendar()
    
    def onPrevMonthClicked(self):
        self._currentMonth -= 1
        self.updateCalendar()

    def onNextMonthClicked(self):
        self._currentMonth += 1
        self.updateCalendar()
    
    def getSelectedDate(self):
        if hasattr(self, 'selectedDate'):
            return self.selectedDate
        return None

    def onDateButtonClicked(self, btn):
        day = int(btn.text())
        self.selectedDate = datetime(self._currentYear, self._currentMonth, day).date()
        self.accept()

