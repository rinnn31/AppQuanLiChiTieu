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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

from ui.widgets.category_donut_chart import CategoryDonutChart
from ui.widgets.financial_comparision_chart import FinancialComparisionChart
from ui.widgets.transaction_viewer import TransactionViewer
import resources.resources_rc

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
"	color: rgb(68, 68, 68);\n"
"}\n"
"")
        self.gridLayout = QGridLayout(OverviewPage)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(15, 15, 15, 15)
        self.comparisionCard = QWidget(OverviewPage)
        self.comparisionCard.setObjectName(u"comparisionCard")
        self.verticalLayout_2 = QVBoxLayout(self.comparisionCard)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 10)
        self.cmpLineChartLb = QLabel(self.comparisionCard)
        self.cmpLineChartLb.setObjectName(u"cmpLineChartLb")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmpLineChartLb.sizePolicy().hasHeightForWidth())
        self.cmpLineChartLb.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.cmpLineChartLb.setFont(font)

        self.verticalLayout_2.addWidget(self.cmpLineChartLb)

        self.cmpChart = FinancialComparisionChart(self.comparisionCard)
        self.cmpChart.setObjectName(u"cmpChart")

        self.verticalLayout_2.addWidget(self.cmpChart)


        self.gridLayout.addWidget(self.comparisionCard, 6, 1, 5, 3)

        self.monthlySummariesCard = QWidget(OverviewPage)
        self.monthlySummariesCard.setObjectName(u"monthlySummariesCard")
        self.verticalLayout = QVBoxLayout(self.monthlySummariesCard)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.monthlySummariesLb = QLabel(self.monthlySummariesCard)
        self.monthlySummariesLb.setObjectName(u"monthlySummariesLb")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.monthlySummariesLb.sizePolicy().hasHeightForWidth())
        self.monthlySummariesLb.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.monthlySummariesLb.setFont(font1)
        self.monthlySummariesLb.setTextFormat(Qt.TextFormat.PlainText)

        self.verticalLayout.addWidget(self.monthlySummariesLb)

        self.donutChartLayout = QHBoxLayout()
        self.donutChartLayout.setObjectName(u"donutChartLayout")
        self.incomePieChart = CategoryDonutChart(self.monthlySummariesCard)
        self.incomePieChart.setObjectName(u"incomePieChart")

        self.donutChartLayout.addWidget(self.incomePieChart)

        self.expensePieChart = CategoryDonutChart(self.monthlySummariesCard)
        self.expensePieChart.setObjectName(u"expensePieChart")

        self.donutChartLayout.addWidget(self.expensePieChart)


        self.verticalLayout.addLayout(self.donutChartLayout)


        self.gridLayout.addWidget(self.monthlySummariesCard, 1, 1, 5, 3)

        self.recentTransactionCard = QWidget(OverviewPage)
        self.recentTransactionCard.setObjectName(u"recentTransactionCard")
        self.verticalLayout_3 = QVBoxLayout(self.recentTransactionCard)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 10)
        self.recentTransactionLb = QLabel(self.recentTransactionCard)
        self.recentTransactionLb.setObjectName(u"recentTransactionLb")
        sizePolicy.setHeightForWidth(self.recentTransactionLb.sizePolicy().hasHeightForWidth())
        self.recentTransactionLb.setSizePolicy(sizePolicy)
        self.recentTransactionLb.setFont(font)

        self.verticalLayout_3.addWidget(self.recentTransactionLb)

        self.transactionTabs = QTabWidget(self.recentTransactionCard)
        self.transactionTabs.setObjectName(u"transactionTabs")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.transactionTabs.sizePolicy().hasHeightForWidth())
        self.transactionTabs.setSizePolicy(sizePolicy2)
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.transactionTabs.setFont(font2)
        self.transactionTabs.setStyleSheet(u"QTabBar::tab {\n"
"    border-bottom-color: #C2C7CB; \n"
"    min-width: 8ex;\n"
"    padding: 3px 10px 3px 10px;\n"
"	color: rgb(83, 83, 83);\n"
"	margin-bottom: 15px\n"
"}\n"
"\n"
"QTabBar::tab:selected{\n"
"	border-bottom: 5px solid rgb(0, 85, 255);\n"
"}\n"
"\n"
"QTabBar::tab:hover:!selected {\n"
"	border-bottom: 5px solid rgb(255, 170, 0)\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"	margin: 0px;\n"
"	border: 5px;\n"
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


        self.gridLayout.addWidget(self.recentTransactionCard, 1, 4, 10, 2)


        self.retranslateUi(OverviewPage)

        self.transactionTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(OverviewPage)
    # setupUi

    def retranslateUi(self, OverviewPage):
        OverviewPage.setWindowTitle(QCoreApplication.translate("OverviewPage", u"Form", None))
        self.cmpLineChartLb.setText(QCoreApplication.translate("OverviewPage", u"So s\u00e1nh thu/chi 30 ng\u00e0y g\u1ea7n nh\u1ea5t", None))
        self.monthlySummariesLb.setText(QCoreApplication.translate("OverviewPage", u"T\u1ed5ng quan thu chi trong th\u00e1ng", None))
        self.recentTransactionLb.setText(QCoreApplication.translate("OverviewPage", u"Giao d\u1ecbch g\u1ea7n \u0111\u00e2y", None))
        self.transactionTabs.setTabText(self.transactionTabs.indexOf(self.allTransTab), QCoreApplication.translate("OverviewPage", u"T\u1ea5t c\u1ea3", None))
        self.transactionTabs.setTabText(self.transactionTabs.indexOf(self.incomeTransTab), QCoreApplication.translate("OverviewPage", u"Thu", None))
        self.transactionTabs.setTabText(self.transactionTabs.indexOf(self.expenseTransTab), QCoreApplication.translate("OverviewPage", u"Chi", None))
    # retranslateUi

