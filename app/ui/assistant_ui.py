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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QStackedWidget, QVBoxLayout, QWidget)
import resources.resources_rc

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
"	border-radius: 21px;\n"
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
"}\n"
"\n"
"#sendBtn, #deleteBtn {\n"
"	background: black;\n"
"	border-radius: 22\n"
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

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.inputTbox = QLineEdit(AssistantPage)
        self.inputTbox.setObjectName(u"inputTbox")
        self.inputTbox.setMinimumSize(QSize(0, 40))
        font = QFont()
        font.setPointSize(12)
        self.inputTbox.setFont(font)
        self.inputTbox.setClearButtonEnabled(False)

        self.horizontalLayout_2.addWidget(self.inputTbox)

        self.sendBtn = QPushButton(AssistantPage)
        self.sendBtn.setObjectName(u"sendBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendBtn.sizePolicy().hasHeightForWidth())
        self.sendBtn.setSizePolicy(sizePolicy)
        self.sendBtn.setMinimumSize(QSize(45, 45))
        self.sendBtn.setMaximumSize(QSize(45, 45))
        self.sendBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/resources/images/white_up.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sendBtn.setIcon(icon)
        self.sendBtn.setIconSize(QSize(25, 25))
        self.sendBtn.setFlat(True)

        self.horizontalLayout_2.addWidget(self.sendBtn)

        self.deleteBtn = QPushButton(AssistantPage)
        self.deleteBtn.setObjectName(u"deleteBtn")
        sizePolicy.setHeightForWidth(self.deleteBtn.sizePolicy().hasHeightForWidth())
        self.deleteBtn.setSizePolicy(sizePolicy)
        self.deleteBtn.setMinimumSize(QSize(45, 45))
        self.deleteBtn.setMaximumSize(QSize(45, 45))
        self.deleteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/resources/images/white_trash.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteBtn.setIcon(icon1)
        self.deleteBtn.setIconSize(QSize(25, 25))
        self.deleteBtn.setFlat(True)

        self.horizontalLayout_2.addWidget(self.deleteBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(AssistantPage)

        QMetaObject.connectSlotsByName(AssistantPage)
    # setupUi

    def retranslateUi(self, AssistantPage):
        AssistantPage.setWindowTitle(QCoreApplication.translate("AssistantPage", u"Form", None))
        self.inputTbox.setPlaceholderText(QCoreApplication.translate("AssistantPage", u"H\u1ecfi tr\u1ee3 l\u00ed \u1ea3o b\u1ea5t c\u1ee9 th\u1ee9 g\u00ec v\u1ec1 t\u00e0i ch\u00ednh", None))
        self.sendBtn.setText("")
        self.deleteBtn.setText("")
    # retranslateUi

