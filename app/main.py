from ui.home import HomeWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

def installExternalResources():
    from PySide6.QtGui import QFontDatabase
    QFontDatabase.addApplicationFont(":/resources/fonts/Roboto-Regular.ttf")
    QFontDatabase.addApplicationFont(":/resources/fonts/Roboto-Bold.ttf")
    QFontDatabase.addApplicationFont(":/resources/Roboto-Medium.ttf")

def scaleWindow(window, screen):
    pass

def main():
    app = QApplication([])
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    installExternalResources()

    window = HomeWindow()
    screen = app.primaryScreen()
    scaleWindow(window, screen)

    window.show()
    
    app.exec()

if __name__ == "__main__":
    main()