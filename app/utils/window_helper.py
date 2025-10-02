from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Qt

class WindowDragHelper(QObject):
    def __init__(self, window : QWidget, handle_widget : QWidget):
        super().__init__(window)
        
        self._window = window
        self._handle_widget = handle_widget
        self._is_dragging = False
        self._drag_position = None

        self._handle_widget.installEventFilter(self)

    def eventFilter(self, watched, event):
        from PySide6.QtCore import Qt, QEvent
        if watched == self._handle_widget:
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self._is_dragging = True
                    self._drag_position = event.globalPosition().toPoint() - self._window.frameGeometry().topLeft()
                    event.accept()
                    return True
            elif event.type() == QEvent.Type.MouseMove:
                if self._is_dragging and event.buttons() & Qt.MouseButton.LeftButton:
                    self._window.move(event.globalPosition().toPoint() - self._drag_position)
                    event.accept()
                    return True
            elif event.type() == QEvent.Type.MouseButtonRelease:
                if event.button() == Qt.MouseButton.LeftButton:
                    self._is_dragging = False
                    event.accept()
                    return True
        return False
    
    def cleanup(self):
        self._handle_widget.removeEventFilter(self)
        self._window = None
        self._handle_widget = None

def install_dragging(window : QWidget, hanlde_widget : QWidget):
    drag_helper = WindowDragHelper(window, hanlde_widget)
    window.setProperty("drag_helper", drag_helper)

def uninstall_dragging(window : QWidget):
    if window.property("drag_helper"):
        window.property("drag_helper").cleanup()
        window.setProperty("drag_helper", None)

def install_drop_shadow(widget : QWidget, radius = 15, color = Qt.GlobalColor.black, offset = (0, 0)):
    from PySide6.QtWidgets import QGraphicsDropShadowEffect
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(radius)
    shadow.setOffset(*offset)
    shadow.setColor(color)
    widget.setGraphicsEffect(shadow)
    widget._drop_shadow_effect = shadow