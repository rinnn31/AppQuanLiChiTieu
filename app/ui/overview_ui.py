# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'overview.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

from app.ui.widgets.quick_area_chart import QuickAreaChart
from app.ui.widgets.quick_donut_chart import QuickDonutChart
from app.ui.widgets.transaction_viewer import TransactionViewer
import app.ui.resources.resources_rc

class Ui_OverviewPage(object):
    def setupUi(self, OverviewPage):
        if not OverviewPage.objectName():
            OverviewPage.setObjectName(u"OverviewPage")
        OverviewPage.resize(1193, 747)
        OverviewPage.setStyleSheet(u"#OverviewPage > QWidget {\n"
"	background-color: white;\n"
"	border-radius: 10px\n"
"}\n"
"\n"
"QLabel {\n"
"	color: rgb(68, 68, 68)\n"
"}\n"
"\n"
"QComboBox {\n"
"    border: 1px solid black;\n"
"    border-radius: 4px;\n"
"    padding: 3px 1px 3px 10px;\n"
"	color: rgb(71, 71, 71)\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"	margin-top: 5px;\n"
"    border: 1px solid black;\n"
"    selection-background-color: lightgray;\n"
"	color: rgb(71, 71, 71);\n"
"	background-color: white;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"	margin: 3px\n"
"}\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"     background: white;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"	color: black;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow { \n"
"	image: url(:/resources/images/black_down_arrow.png);\n"
"	width: 13px;\n"
"	height: 13px;\n"
""
                        "	right: 5px\n"
"}\n"
"\n"
"QComboBox::down-arrow:on {\n"
"	image: url(:/resources/images/black_up_arrow.png);\n"
"}")
        self.gridLayout = QGridLayout(OverviewPage)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 15, -1, 15)
        self.comparisionCard = QWidget(OverviewPage)
        self.comparisionCard.setObjectName(u"comparisionCard")
        self.verticalLayout_2 = QVBoxLayout(self.comparisionCard)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 10)
        self.horizontalWidget = QWidget(self.comparisionCard)
        self.horizontalWidget.setObjectName(u"horizontalWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget.sizePolicy().hasHeightForWidth())
        self.horizontalWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cmpLineChartLb = QLabel(self.horizontalWidget)
        self.cmpLineChartLb.setObjectName(u"cmpLineChartLb")
        sizePolicy.setHeightForWidth(self.cmpLineChartLb.sizePolicy().hasHeightForWidth())
        self.cmpLineChartLb.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.cmpLineChartLb.setFont(font)

        self.horizontalLayout_2.addWidget(self.cmpLineChartLb)

        self.comparisionCbox = QComboBox(self.horizontalWidget)
        self.comparisionCbox.setObjectName(u"comparisionCbox")
        self.comparisionCbox.setMinimumSize(QSize(150, 0))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.comparisionCbox.setFont(font1)

        self.horizontalLayout_2.addWidget(self.comparisionCbox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.horizontalWidget)

        self.incomeAreaChart = QuickAreaChart(self.comparisionCard)
        self.incomeAreaChart.setObjectName(u"incomeAreaChart")

        self.verticalLayout_2.addWidget(self.incomeAreaChart)

        self.expenseAreaChart = QuickAreaChart(self.comparisionCard)
        self.expenseAreaChart.setObjectName(u"expenseAreaChart")

        self.verticalLayout_2.addWidget(self.expenseAreaChart)


        self.gridLayout.addWidget(self.comparisionCard, 4, 1, 5, 2)

        self.recentTransactCard = QWidget(OverviewPage)
        self.recentTransactCard.setObjectName(u"recentTransactCard")
        self.verticalLayout_3 = QVBoxLayout(self.recentTransactCard)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 10)
        self.recentTransactLb = QLabel(self.recentTransactCard)
        self.recentTransactLb.setObjectName(u"recentTransactLb")
        sizePolicy.setHeightForWidth(self.recentTransactLb.sizePolicy().hasHeightForWidth())
        self.recentTransactLb.setSizePolicy(sizePolicy)
        self.recentTransactLb.setFont(font)

        self.verticalLayout_3.addWidget(self.recentTransactLb)

        self.transactionTabs = QTabWidget(self.recentTransactCard)
        self.transactionTabs.setObjectName(u"transactionTabs")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.transactionTabs.sizePolicy().hasHeightForWidth())
        self.transactionTabs.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.transactionTabs.setFont(font2)
        self.transactionTabs.setStyleSheet(u"QTabBar::tab {\n"
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
        self.transactionTabs.setTabShape(QTabWidget.TabShape.Rounded)
        self.transactionTabs.setElideMode(Qt.TextElideMode.ElideNone)
        self.allTransTab = TransactionViewer()
        self.allTransTab.setObjectName(u"allTransTab")
        self.transactionTabs.addTab(self.allTransTab, "")
        self.incomeTransTab = TransactionViewer()
        self.incomeTransTab.setObjectName(u"incomeTransTab")
        self.transactionTabs.addTab(self.incomeTransTab, "")
        self.expenseTransTab = TransactionViewer()
        self.expenseTransTab.setObjectName(u"expenseTransTab")
        self.transactionTabs.addTab(self.expenseTransTab, "")

        self.verticalLayout_3.addWidget(self.transactionTabs)


        self.gridLayout.addWidget(self.recentTransactCard, 1, 3, 8, 1)

        self.periodicFinCard = QWidget(OverviewPage)
        self.periodicFinCard.setObjectName(u"periodicFinCard")
        self.verticalLayout = QVBoxLayout(self.periodicFinCard)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 10)
        self.horizontalWidget1 = QWidget(self.periodicFinCard)
        self.horizontalWidget1.setObjectName(u"horizontalWidget1")
        sizePolicy.setHeightForWidth(self.horizontalWidget1.sizePolicy().hasHeightForWidth())
        self.horizontalWidget1.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.horizontalWidget1)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.periodicFinLb = QLabel(self.horizontalWidget1)
        self.periodicFinLb.setObjectName(u"periodicFinLb")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.periodicFinLb.sizePolicy().hasHeightForWidth())
        self.periodicFinLb.setSizePolicy(sizePolicy2)
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        font3.setItalic(False)
        font3.setStrikeOut(False)
        font3.setKerning(True)
        self.periodicFinLb.setFont(font3)
        self.periodicFinLb.setTextFormat(Qt.TextFormat.PlainText)

        self.horizontalLayout.addWidget(self.periodicFinLb)

        self.periodicCbox = QComboBox(self.horizontalWidget1)
        self.periodicCbox.setObjectName(u"periodicCbox")
        self.periodicCbox.setMinimumSize(QSize(120, 0))
        self.periodicCbox.setMaximumSize(QSize(120, 16777215))
        self.periodicCbox.setFont(font1)

        self.horizontalLayout.addWidget(self.periodicCbox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.horizontalWidget1)

        self.periodicFinMainlayout = QHBoxLayout()
        self.periodicFinMainlayout.setObjectName(u"periodicFinMainlayout")
        self.incomePieChart = QuickDonutChart(self.periodicFinCard)
        self.incomePieChart.setObjectName(u"incomePieChart")

        self.periodicFinMainlayout.addWidget(self.incomePieChart)

        self.expensePieChart = QuickDonutChart(self.periodicFinCard)
        self.expensePieChart.setObjectName(u"expensePieChart")

        self.periodicFinMainlayout.addWidget(self.expensePieChart)


        self.verticalLayout.addLayout(self.periodicFinMainlayout)


        self.gridLayout.addWidget(self.periodicFinCard, 1, 1, 3, 2)


        self.retranslateUi(OverviewPage)

        self.transactionTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(OverviewPage)
    # setupUi

    def retranslateUi(self, OverviewPage):
        OverviewPage.setWindowTitle(QCoreApplication.translate("OverviewPage", u"Form", None))
        self.cmpLineChartLb.setText(QCoreApplication.translate("OverviewPage", u"So s\u00e1nh thu/chi", None))
        self.recentTransactLb.setText(QCoreApplication.translate("OverviewPage", u"Giao d\u1ecbch g\u1ea7n \u0111\u00e2y", None))
        self.transactionTabs.setTabText(self.transactionTabs.indexOf(self.allTransTab), QCoreApplication.translate("OverviewPage", u"T\u1ea5t c\u1ea3", None))
        self.transactionTabs.setTabText(self.transactionTabs.indexOf(self.incomeTransTab), QCoreApplication.translate("OverviewPage", u"Thu", None))
        self.transactionTabs.setTabText(self.transactionTabs.indexOf(self.expenseTransTab), QCoreApplication.translate("OverviewPage", u"Chi", None))
        self.periodicFinLb.setText(QCoreApplication.translate("OverviewPage", u"Thu chi \u0111\u1ecbnh k\u1ef3", None))
    # retranslateUi

