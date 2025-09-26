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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1132, 707)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.panelWidget = QWidget(self.centralwidget)
        self.panelWidget.setObjectName(u"panelWidget")
        self.panelLayout = QVBoxLayout(self.panelWidget)
        self.panelLayout.setObjectName(u"panelLayout")
        self.pushButton_4 = QPushButton(self.panelWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.panelLayout.addWidget(self.pushButton_4)

        self.overviewBtn = QPushButton(self.panelWidget)
        self.overviewBtn.setObjectName(u"overviewBtn")

        self.panelLayout.addWidget(self.overviewBtn)

        self.managementBtn = QPushButton(self.panelWidget)
        self.managementBtn.setObjectName(u"managementBtn")

        self.panelLayout.addWidget(self.managementBtn)

        self.chatBtn = QPushButton(self.panelWidget)
        self.chatBtn.setObjectName(u"chatBtn")

        self.panelLayout.addWidget(self.chatBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.panelLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.panelWidget)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setObjectName(u"mainLayout")

        self.horizontalLayout.addLayout(self.mainLayout)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ChiTi\u00eau+", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.overviewBtn.setText(QCoreApplication.translate("MainWindow", u"T\u1ed5ng quan", None))
        self.managementBtn.setText(QCoreApplication.translate("MainWindow", u"Qu\u1ea3n l\u00ed", None))
        self.chatBtn.setText(QCoreApplication.translate("MainWindow", u"Chat v\u1edbi tr\u1ee3 l\u00ed \u1ea3o", None))
    # retranslateUi

