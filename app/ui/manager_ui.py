# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manager.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

from ui.widgets.finance_calendar import FinanceCalendar
from ui.widgets.transaction_viewer import TransactionViewer
import resources.resources_rc

class Ui_ManagerPage(object):
    def setupUi(self, ManagerPage):
        if not ManagerPage.objectName():
            ManagerPage.setObjectName(u"ManagerPage")
        ManagerPage.resize(1056, 665)
        ManagerPage.setStyleSheet(u"\n"
"#ManagerPage > QWidget {\n"
"	background: white;\n"
"	border-radius: 10px\n"
"}\n"
"\n"
"QLabel {\n"
"	color: black\n"
"}\n"
"\n"
"#transactionEditorLb {\n"
"	margin-bottom: 20px\n"
"}\n"
"\n"
"#addIncomeBtn {\n"
"	background: rgb(24, 179, 0)\n"
"}\n"
"\n"
"#addExpenseBtn {\n"
"	background: rgb(217, 0, 4)\n"
"}\n"
"\n"
"#findBtn {\n"
"	background: rgb(10, 182, 209)\n"
"}")
        self.gridLayout = QGridLayout(ManagerPage)
        self.gridLayout.setSpacing(15)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalWidget = QWidget(ManagerPage)
        self.verticalWidget.setObjectName(u"verticalWidget")
        self.verticalLayout_2 = QVBoxLayout(self.verticalWidget)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(15, 15, 15, -1)
        self.transactionEditorLb = QLabel(self.verticalWidget)
        self.transactionEditorLb.setObjectName(u"transactionEditorLb")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transactionEditorLb.sizePolicy().hasHeightForWidth())
        self.transactionEditorLb.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.transactionEditorLb.setFont(font)
        self.transactionEditorLb.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.transactionEditorLb)

        self.widget = QWidget(self.verticalWidget)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.addIncomeBtn = QPushButton(self.widget)
        self.addIncomeBtn.setObjectName(u"addIncomeBtn")
        self.addIncomeBtn.setMinimumSize(QSize(0, 40))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.addIncomeBtn.setFont(font1)
        icon = QIcon()
        icon.addFile(u":/resources/images/white_income.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addIncomeBtn.setIcon(icon)
        self.addIncomeBtn.setIconSize(QSize(22, 22))
        self.addIncomeBtn.setFlat(True)

        self.horizontalLayout.addWidget(self.addIncomeBtn)

        self.addExpenseBtn = QPushButton(self.widget)
        self.addExpenseBtn.setObjectName(u"addExpenseBtn")
        self.addExpenseBtn.setMinimumSize(QSize(0, 40))
        self.addExpenseBtn.setFont(font1)
        icon1 = QIcon()
        icon1.addFile(u":/resources/images/white_expense.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addExpenseBtn.setIcon(icon1)
        self.addExpenseBtn.setIconSize(QSize(22, 22))
        self.addExpenseBtn.setFlat(True)

        self.horizontalLayout.addWidget(self.addExpenseBtn)


        self.verticalLayout_2.addWidget(self.widget)

        self.findBtn = QPushButton(self.verticalWidget)
        self.findBtn.setObjectName(u"findBtn")
        self.findBtn.setMinimumSize(QSize(0, 40))
        self.findBtn.setFont(font1)
        icon2 = QIcon()
        icon2.addFile(u":/resources/images/white_transaction_find.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.findBtn.setIcon(icon2)
        self.findBtn.setIconSize(QSize(22, 22))
        self.findBtn.setFlat(True)

        self.verticalLayout_2.addWidget(self.findBtn)


        self.gridLayout.addWidget(self.verticalWidget, 0, 6, 3, 4)

        self.verticalWidget_2 = QWidget(ManagerPage)
        self.verticalWidget_2.setObjectName(u"verticalWidget_2")
        self.verticalLayout_3 = QVBoxLayout(self.verticalWidget_2)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(15, 20, 15, -1)
        self.label = QLabel(self.verticalWidget_2)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.verticalLayout_3.addWidget(self.label)

        self.tabWidget = QTabWidget(self.verticalWidget_2)
        self.tabWidget.setObjectName(u"tabWidget")
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.tabWidget.setFont(font2)
        self.tabWidget.setStyleSheet(u"QTabBar::tab {\n"
"    border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"    min-width: 8ex;\n"
"    padding: 3px 10px 3px 10px;\n"
"	color: rgb(83, 83, 83);\n"
"	margin-bottom: 15px\n"
"}\n"
"\n"
"QTabBar::tab:selected{\n"
"	border-bottom: 5px solid rgb(0, 85, 255)\n"
"}\n"
"\n"
"QTabBar::tab:hover:!selected {\n"
"	border-bottom: 5px solid rgb(255, 170, 0)\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"	margin: 0px;\n"
"	border: 0px\n"
"}")
        self.expenseTab = TransactionViewer()
        self.expenseTab.setObjectName(u"expenseTab")
        self.tabWidget.addTab(self.expenseTab, "")
        self.incomeTab = TransactionViewer()
        self.incomeTab.setObjectName(u"incomeTab")
        self.tabWidget.addTab(self.incomeTab, "")

        self.verticalLayout_3.addWidget(self.tabWidget)


        self.gridLayout.addWidget(self.verticalWidget_2, 3, 6, 7, 4)

        self.verticalWidget1 = QWidget(ManagerPage)
        self.verticalWidget1.setObjectName(u"verticalWidget1")
        self.verticalLayout = QVBoxLayout(self.verticalWidget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.calendar = FinanceCalendar(self.verticalWidget1)
        self.calendar.setObjectName(u"calendar")

        self.verticalLayout.addWidget(self.calendar)


        self.gridLayout.addWidget(self.verticalWidget1, 0, 0, 10, 6)


        self.retranslateUi(ManagerPage)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ManagerPage)
    # setupUi

    def retranslateUi(self, ManagerPage):
        ManagerPage.setWindowTitle(QCoreApplication.translate("ManagerPage", u"Form", None))
        self.transactionEditorLb.setText(QCoreApplication.translate("ManagerPage", u"Ch\u1ec9nh s\u1eeda giao d\u1ecbch", None))
        self.addIncomeBtn.setText(QCoreApplication.translate("ManagerPage", u"  Th\u00eam kho\u1ea3n thu", None))
        self.addExpenseBtn.setText(QCoreApplication.translate("ManagerPage", u"  Th\u00eam kho\u1ea3n chi", None))
        self.findBtn.setText(QCoreApplication.translate("ManagerPage", u"  T\u00ecm ki\u1ebfm giao d\u1ecbch", None))
        self.label.setText(QCoreApplication.translate("ManagerPage", u"L\u1ecbch s\u1eed giao d\u1ecbch trong ng\u00e0y", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.expenseTab), QCoreApplication.translate("ManagerPage", u"Thu", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.incomeTab), QCoreApplication.translate("ManagerPage", u"Chi", None))
    # retranslateUi

