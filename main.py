from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QIcon
from dotenv import load_dotenv
import os
import sys
from app.ui.home import HomeWindow
from app.database.transaction_manager import TransactionManager

class FinancialApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.setApplicationName("Chi Tiêu+")
        self.setWindowIcon(QIcon(":/resources/icons/app_icon.png"))
        
        self.installExternalResources()

        self.transactionManager = TransactionManager()

    def getTransactionManager(self):
        return self.transactionManager

    def run(self):
        window = HomeWindow()
        window.show()
        self.exec()

    def installExternalResources(self):
        from PySide6.QtGui import QFontDatabase
        QFontDatabase.addApplicationFont(":/resources/fonts/Roboto-Regular.ttf")
        QFontDatabase.addApplicationFont(":/resources/fonts/Roboto-Bold.ttf")
        QFontDatabase.addApplicationFont(":/resources/Roboto-Medium.ttf")


if __name__ == "__main__":
    load_dotenv()
    geminiKey = os.getenv("GEMINI_API_KEY")
    if not geminiKey:
        print("Warning: GEMINI_API_KEY not found in environment variables. Chatbot functionality may be limited.")

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    FinancialApp.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = FinancialApp(sys.argv)
    app.run()