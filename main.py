#!/usr/bin/env python3
"""
Simple Chat View example using PyQt5.
Features:
- Left (incoming) and right (outgoing) message bubbles
- Scrollable chat area that keeps view at bottom
- Message input with Send button and Enter to send
- Message bubble widgets with word wrap and max width (~50% of window)
- Timestamps

Run: python pyqt_chat_view.py
Requires: PyQt5 (pip install PyQt5)
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QScrollArea, QLabel, QSizePolicy, QLineEdit, QFrame
)
from PySide6.QtCore import Qt, QTimer, QDateTime
from PySide6.QtGui import QFont, QPalette


class MessageBubble(QFrame):
    def __init__(self, text: str, right: bool = False, parent=None):
        super().__init__(parent)
        self.right = right
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.setFrameShape(QFrame.NoFrame)

        # layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        # message label
        label = QLabel()
        label.setText(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        label.setFont(QFont("Segoe UI", 10))

        # timestamp
        ts = QLabel(QDateTime.currentDateTime().toString("HH:mm"))
        ts.setAlignment(Qt.AlignRight)
        ts.setFont(QFont("Segoe UI", 8))
        ts.setStyleSheet("color: gray;")

        layout.addWidget(label)
        layout.addWidget(ts)

        # styling
        if right:
            self.setStyleSheet(
                "QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b3e5fc, stop:1 #81d4fa);"
                " border-radius: 10px; margin:6px; padding:4px; }"
            )
        else:
            self.setStyleSheet(
                "QFrame { background: #f1f0f0; border-radius: 10px; margin:6px; padding:4px; }"
            )

    def maximumSizeHint(self):
        # limit bubble width to ~50% of parent width
        if self.parent() is not None:
            w = self.parent().width() * 0.5
            return super().maximumSizeHint().expandedTo(self.sizeHint()).boundedTo(Qt.QSize(int(w), 16777215))
        return super().maximumSizeHint()


class ChatView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat View - PyQt5 Example")
        self.resize(640, 480)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)

        # Scroll area for messages
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.container = QWidget()
        self.vbox = QVBoxLayout(self.container)
        self.vbox.setAlignment(Qt.AlignTop)
        self.vbox.setSpacing(2)
        self.container.setLayout(self.vbox)

        self.scroll.setWidget(self.container)
        main_layout.addWidget(self.scroll)

        # Input area
        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a message...")
        self.input.returnPressed.connect(self.on_send)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.on_send)

        input_layout.addWidget(self.input)
        input_layout.addWidget(send_btn)

        main_layout.addLayout(input_layout)

        # seed with some messages
        QTimer.singleShot(100, lambda: self.add_message("Hello! This is an incoming message.", right=False))
        QTimer.singleShot(250, lambda: self.add_message("Hi! This is an outgoing message.\nIt can wrap across multiple lines.", right=True))

    def add_message(self, text: str, right: bool = False):
        # container for alignment
        holder = QWidget()
        h = QHBoxLayout(holder)
        h.setContentsMargins(6, 2, 6, 2)

        if right:
            h.addStretch()
            bubble = MessageBubble(text, right=True, parent=self.container)
            bubble.setMaximumWidth(int(self.width() * 0.5))
            h.addWidget(bubble, 0, Qt.AlignRight)
        else:
            bubble = MessageBubble(text, right=False, parent=self.container)
            bubble.setMaximumWidth(int(self.width() * 0.5))
            h.addWidget(bubble, 0, Qt.AlignLeft)
            h.addStretch()

        self.vbox.addWidget(holder)
        QTimer.singleShot(0, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

    def on_send(self):
        text = self.input.text().strip()
        if not text:
            return
        self.add_message(text, right=True)
        self.input.clear()

        # simulate a reply after a short delay
        QTimer.singleShot(600, lambda: self.add_message("Auto-reply: got your message!", right=False))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ChatView()
    w.show()
    sys.exit(app.exec_())
