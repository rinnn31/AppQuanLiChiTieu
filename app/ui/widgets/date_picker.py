from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QGridLayout, QLabel
from PySide6.QtCore import Qt, QDate
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.utils.window_helper import applyDropShadow
class DatePicker(QDialog):
    def __init__(self, parent=None, lowerDate=None, upperDate=None):
        super().__init__(parent)
        self._lowerDate = lowerDate if lowerDate else datetime(2000, 1, 1).date()
        self._upperDate = upperDate if upperDate else datetime.now().date()
        self._selectedDate = datetime.now().date()
        self.setupUi()
        self.updateCalendar()

    def setupUi(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            #container {
                background: white;
                border-radius: 10px;
            }
            #prevBtn, #nextBtn {
                background: white;
                border: none;
                border-radius: 8px;
                icon-size: 16px;
                min-width: 24px;
                min-height: 24px;
                max-width: 24px;
                max-height: 24px;
            }
                           
            #prevBtn {
                icon: url(:/resources/images/black_left_arrow.png);
            }
                           
            #nextBtn {
                icon: url(:/resources/images/black_right_arrow.png);
            }
                           
            #prevBtn:hover, #nextBtn:hover {
                background: #f0f0f0;
            }
                           
            #dateBtn {
                background: white;
                border: none;
                border-radius: 8px;
                color: black;
                font: 9pt "Roboto";
            }
                           
            #dateBtn:hover {
                background: #3c81e8;
                color: white;
            }
                           
            #dateBtn:!enabled {
                color: gray;
            }

            QLabel {
                color: black;
                font: bold 10pt "Roboto";
                text-align: center;
            }       
        """)

        self._container = QWidget(self)
        self._container.setObjectName("container")
        applyDropShadow(self._container, radius=5)

        layout = QVBoxLayout(self._container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        yearLayout = QHBoxLayout()
        yearLayout.setContentsMargins(10,0,10,0)
        self._prevYearBtn = QPushButton(flat=True)
        self._prevYearBtn.setObjectName("prevBtn")
        self._prevYearBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._prevYearBtn.clicked.connect(self.onPrevYearClicked)

        self._nextYearBtn = QPushButton(flat=True)
        self._nextYearBtn.setObjectName("nextBtn")
        self._nextYearBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._nextYearBtn.clicked.connect(self.onNextYearClicked)

        self._yearLb = QLabel()

        yearLayout.addWidget(self._prevYearBtn)
        yearLayout.addStretch()
        yearLayout.addWidget(self._yearLb)
        yearLayout.addStretch()
        yearLayout.addWidget(self._nextYearBtn)

        monthLayout = QHBoxLayout()
        monthLayout.setContentsMargins(10,0,10,0)

        self._prevMonthBtn = QPushButton(flat=True)
        self._prevMonthBtn.setObjectName("prevBtn")
        self._prevMonthBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._prevMonthBtn.clicked.connect(self.onPrevMonthClicked)

        self._nextMonthBtn = QPushButton(flat=True)
        self._nextMonthBtn.setObjectName("nextBtn")
        self._nextMonthBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._nextMonthBtn.clicked.connect(self.onNextMonthClicked)

        self._monthLb = QLabel()

        monthLayout.addWidget(self._prevMonthBtn)
        monthLayout.addStretch()
        monthLayout.addWidget(self._monthLb)
        monthLayout.addStretch()
        monthLayout.addWidget(self._nextMonthBtn)
    
        self._dayGridLayout = QGridLayout()
        self._dayGridLayout.setSpacing(5)
        days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        for i, day in enumerate(days):
            dayLb = QLabel(day)
            dayLb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._dayGridLayout.addWidget(dayLb, 0, i)
        for week in range(1, 6):
            for day in range(7):
                dateBtn = QPushButton(str(week * 7 + day - 6), flat=True) 
                dateBtn.setObjectName("dateBtn")
                dateBtn.setCursor(Qt.CursorShape.PointingHandCursor)
                dateBtn.setFixedSize(30, 30)
                dateBtn.clicked.connect(lambda checked, btn=dateBtn: self.onDateButtonClicked(btn))
                self._dayGridLayout.addWidget(dateBtn, week, day)
        
        layout.addLayout(yearLayout)
        layout.addLayout(monthLayout)
        layout.addLayout(self._dayGridLayout)

        self.setFixedSize(300, 350)

    def resizeEvent(self, arg__1):
        super().resizeEvent(arg__1)
        self._container.setGeometry(5, 5, self.width()-10, self.height()-10)
    
    def updateCalendar(self):
        if self._selectedDate < self._lowerDate:
            self._selectedDate = self._lowerDate
        if self._selectedDate > self._upperDate:
            self._selectedDate = self._upperDate
        
        self._prevYearBtn.setEnabled(self._selectedDate.year > self._lowerDate.year)
        self._nextYearBtn.setEnabled(self._selectedDate.year < self._upperDate.year)
        self._prevMonthBtn.setEnabled(not (self._selectedDate.year == self._lowerDate.year and self._selectedDate.month == self._lowerDate.month))
        self._nextMonthBtn.setEnabled(not (self._selectedDate.year == self._upperDate.year and self._selectedDate.month == self._upperDate.month))
    
        self._fillCalendar()

    def _fillCalendar(self):
        self._yearLb.setText(str(self._selectedDate.year))
        self._monthLb.setText(f"Tháng {self._selectedDate.month}")

        firstDayOfMonth = QDate(self._selectedDate.year, self._selectedDate.month, 1)
        startDayOfWeek = firstDayOfMonth.dayOfWeek()
        startDate = firstDayOfMonth.addDays(- (startDayOfWeek - 1) )

        for i in range(1, 6):
            for j in range(7):
                dateBtn = self._dayGridLayout.itemAtPosition(i, j).widget()
                currentDate = startDate.addDays((i - 1) * 7 + j)
                dateBtn.setText(str(currentDate.day()))
                dateBtn.setEnabled(self._lowerDate <= currentDate.toPython() <= self._upperDate and currentDate.month() == self._selectedDate.month)

    def onPrevYearClicked(self):
        self._selectedDate += relativedelta(years=-1)
        self.updateCalendar()

    def onNextYearClicked(self):
        self._selectedDate += relativedelta(years=1)
        self.updateCalendar()
    
    def onPrevMonthClicked(self):
        self._selectedDate += relativedelta(months=-1)
        self.updateCalendar()

    def onNextMonthClicked(self):
        self._selectedDate += relativedelta(months=1)
        self.updateCalendar()
    
    def getSelectedDate(self):
        return self._selectedDate

    def onDateButtonClicked(self, btn):
        day = int(btn.text())
        self._selectedDate = self._selectedDate.replace(day=day)
        self.accept()

