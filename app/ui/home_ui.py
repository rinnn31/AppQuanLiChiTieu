# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)
import resources.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.WindowModal)
        MainWindow.resize(1544, 862)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QScrollBar\n"
"{\n"
"	background-color: rgb(180, 180, 180);\n"
"	border:1px transparent;\n"
"	border-radius:3px;\n"
"}\n"
"QScrollBar::handle\n"
"{\n"
"	background-color: rgb(122, 122, 122);\n"
"	border-radius:3px;\n"
"}\n"
"QScrollBar::sub-page\n"
"{\n"
"	background: none;\n"
"	width: 0px;\n"
"	height: 0px;\n"
"}\n"
"QScrollBar::add-page\n"
"{\n"
"	background: none;\n"
"	width: 0px;\n"
"	height: 0px;\n"
"}\n"
"\n"
"QScrollBar::sub-line\n"
"{\n"
"	background: none;\n"
"	width: 0px;\n"
"	height: 0px;\n"
"}\n"
"QScrollBar::add-line\n"
"{\n"
"	background: none;\n"
"	width: 0px;\n"
"	height: 0px;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"	witdh: 6px;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"	height: 6px\n"
"}")
        self.windowWidget = QWidget(MainWindow)
        self.windowWidget.setObjectName(u"windowWidget")
        self.windowWidget.setStyleSheet(u"#windowWidget {\n"
"	background-color: rgb(240, 240, 240);\n"
"	border: 0px;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"#navigationPanel {\n"
"	background-color: rgb(29, 29, 29);\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"#appLogo {\n"
"	margin-bottom: 30px;\n"
"	margin-top:30px\n"
"}\n"
"\n"
"#navigationPanel > QPushButton {\n"
"	background-color: rgb(29, 29, 29);\n"
"	color: rgb(240, 240, 240);\n"
"	text-align: left;\n"
"	padding-left: 20px;\n"
"	\n"
"}\n"
"\n"
"#navigationPanel > QPushButton[selected=\"true\"] {\n"
"	background-color: rgb(21, 142, 176)\n"
"}\n"
"\n"
"#mainLayout {\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-right-radius:10px\n"
"}\n"
"#titlePanel {\n"
"	background-color: rgb(240, 240, 240);\n"
"	border-top-right-radius: 10px\n"
"}\n"
"\n"
"#pageNameLb {\n"
"	color: rgb(0,0,0);\n"
"}\n"
"\n"
"#closeBtn {\n"
"	color: rgb(0,0,0);\n"
"	background-color: rgb(240, 240, 240);\n"
"}\n"
"\n"
"#pageContainer {\n"
"	background-color : rgb(240, 240, 240);\n"
"	border-bottom-right-radius:10px\n"
""
                        "}")
        self.horizontalLayout = QHBoxLayout(self.windowWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.navigationPanel = QWidget(self.windowWidget)
        self.navigationPanel.setObjectName(u"navigationPanel")
        self.navigationPanel.setMinimumSize(QSize(300, 0))
        self.navigationPanel.setMaximumSize(QSize(300, 16777215))
        self.panelLayout = QVBoxLayout(self.navigationPanel)
        self.panelLayout.setObjectName(u"panelLayout")
        self.panelLayout.setContentsMargins(10, 10, 10, -1)
        self.appLogo = QLabel(self.navigationPanel)
        self.appLogo.setObjectName(u"appLogo")
        self.appLogo.setMinimumSize(QSize(280, 150))
        self.appLogo.setMaximumSize(QSize(280, 150))
        self.appLogo.setTextFormat(Qt.TextFormat.MarkdownText)
        self.appLogo.setPixmap(QPixmap(u":/resources/images/logo.png"))
        self.appLogo.setScaledContents(True)

        self.panelLayout.addWidget(self.appLogo)

        self.overviewBtn = QPushButton(self.navigationPanel)
        self.overviewBtn.setObjectName(u"overviewBtn")
        self.overviewBtn.setMinimumSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.overviewBtn.setFont(font)
        icon = QIcon()
        icon.addFile(u":/resources/images/white_dashboard.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.overviewBtn.setIcon(icon)
        self.overviewBtn.setIconSize(QSize(32, 32))
        self.overviewBtn.setFlat(True)
        self.overviewBtn.setProperty(u"selected", True)

        self.panelLayout.addWidget(self.overviewBtn)

        self.managerBtn = QPushButton(self.navigationPanel)
        self.managerBtn.setObjectName(u"managerBtn")
        self.managerBtn.setMinimumSize(QSize(0, 50))
        self.managerBtn.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u":/resources/images/white_wallet.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.managerBtn.setIcon(icon1)
        self.managerBtn.setIconSize(QSize(32, 32))
        self.managerBtn.setFlat(True)
        self.managerBtn.setProperty(u"selected", True)

        self.panelLayout.addWidget(self.managerBtn)

        self.chatBtn = QPushButton(self.navigationPanel)
        self.chatBtn.setObjectName(u"chatBtn")
        self.chatBtn.setMinimumSize(QSize(0, 50))
        self.chatBtn.setFont(font)
        icon2 = QIcon()
        icon2.addFile(u":/resources/images/white_chatbot.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.chatBtn.setIcon(icon2)
        self.chatBtn.setIconSize(QSize(32, 32))
        self.chatBtn.setCheckable(False)
        self.chatBtn.setFlat(True)
        self.chatBtn.setProperty(u"selected", True)

        self.panelLayout.addWidget(self.chatBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.panelLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.navigationPanel)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.titlePanel = QWidget(self.windowWidget)
        self.titlePanel.setObjectName(u"titlePanel")
        self.titlePanel.setMinimumSize(QSize(0, 40))
        self.titlePanel.setMaximumSize(QSize(16777215, 40))
        self.titlePanelLayout = QHBoxLayout(self.titlePanel)
        self.titlePanelLayout.setObjectName(u"titlePanelLayout")
        self.titlePanelLayout.setContentsMargins(20, 0, 10, 0)
        self.pageIconLb = QLabel(self.titlePanel)
        self.pageIconLb.setObjectName(u"pageIconLb")
        self.pageIconLb.setMinimumSize(QSize(40, 0))
        self.pageIconLb.setMaximumSize(QSize(40, 16777215))

        self.titlePanelLayout.addWidget(self.pageIconLb)

        self.pageNameLb = QLabel(self.titlePanel)
        self.pageNameLb.setObjectName(u"pageNameLb")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageNameLb.sizePolicy().hasHeightForWidth())
        self.pageNameLb.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.pageNameLb.setFont(font1)

        self.titlePanelLayout.addWidget(self.pageNameLb)

        self.closeBtn = QPushButton(self.titlePanel)
        self.closeBtn.setObjectName(u"closeBtn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.closeBtn.sizePolicy().hasHeightForWidth())
        self.closeBtn.setSizePolicy(sizePolicy1)
        self.closeBtn.setMinimumSize(QSize(40, 40))
        self.closeBtn.setMaximumSize(QSize(40, 40))
        self.closeBtn.setAutoFillBackground(False)
        icon3 = QIcon()
        icon3.addFile(u":/resources/images/black_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeBtn.setIcon(icon3)
        self.closeBtn.setIconSize(QSize(32, 32))
        self.closeBtn.setFlat(True)

        self.titlePanelLayout.addWidget(self.closeBtn)


        self.mainLayout.addWidget(self.titlePanel)

        self.pageContainer = QStackedWidget(self.windowWidget)
        self.pageContainer.setObjectName(u"pageContainer")
        self.pageContainerPage1 = QWidget()
        self.pageContainerPage1.setObjectName(u"pageContainerPage1")
        self.pageContainerLayout = QVBoxLayout(self.pageContainerPage1)
        self.pageContainerLayout.setObjectName(u"pageContainerLayout")
        self.pageContainer.addWidget(self.pageContainerPage1)

        self.mainLayout.addWidget(self.pageContainer)


        self.horizontalLayout.addLayout(self.mainLayout)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        MainWindow.setCentralWidget(self.windowWidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ChiTi\u00eau+", None))
        self.appLogo.setText("")
        self.overviewBtn.setText(QCoreApplication.translate("MainWindow", u"   T\u1ed5ng quan", None))
        self.managerBtn.setText(QCoreApplication.translate("MainWindow", u"   Qu\u1ea3n l\u00ed", None))
        self.chatBtn.setText(QCoreApplication.translate("MainWindow", u"   Chat v\u1edbi tr\u1ee3 l\u00ed \u1ea3o", None))
        self.pageIconLb.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pageNameLb.setText(QCoreApplication.translate("MainWindow", u"T\u1ed5ng quan", None))
        self.closeBtn.setText("")
    # retranslateUi

