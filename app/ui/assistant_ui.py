# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assistant.ui'
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
from PySide6.QtWidgets import (QApplication, QLineEdit, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_AssistantPage(object):
    def setupUi(self, AssistantPage):
        if not AssistantPage.objectName():
            AssistantPage.setObjectName(u"AssistantPage")
        AssistantPage.resize(996, 614)
        AssistantPage.setStyleSheet(u"#AssistantPage {\n"
"	background: white\n"
"}\n"
"\n"
"#inputTbox {\n"
"	background: white;\n"
"	border: 2px solid gray;\n"
"	border-radius: 23px;\n"
"	color: black;\n"
"	padding: 10px 20px;\n"
"}\n"
"\n"
"#chatContainer {\n"
"	background: white;\n"
"}\n"
"\n"
"#inputTbox:focus {\n"
"	border: 1px solid #0AB6D1;\n"
"}")
        self.verticalLayout = QVBoxLayout(AssistantPage)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(25, -1, 25, 15)
        self.chatContainer = QStackedWidget(AssistantPage)
        self.chatContainer.setObjectName(u"chatContainer")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.chatContainer.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.chatContainer.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.chatContainer)

        self.inputTbox = QLineEdit(AssistantPage)
        self.inputTbox.setObjectName(u"inputTbox")
        self.inputTbox.setMinimumSize(QSize(0, 40))
        font = QFont()
        font.setPointSize(12)
        self.inputTbox.setFont(font)
        self.inputTbox.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.inputTbox)


        self.retranslateUi(AssistantPage)

        QMetaObject.connectSlotsByName(AssistantPage)
    # setupUi

    def retranslateUi(self, AssistantPage):
        AssistantPage.setWindowTitle(QCoreApplication.translate("AssistantPage", u"Form", None))
        self.inputTbox.setPlaceholderText(QCoreApplication.translate("AssistantPage", u"H\u1ecfi tr\u1ee3 l\u00ed \u1ea3o b\u1ea5t c\u1ee9 th\u1ee9 g\u00ec v\u1ec1 t\u00e0i ch\u00ednh", None))
    # retranslateUi

