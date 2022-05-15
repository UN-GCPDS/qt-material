from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from qt_material import apply_stylesheet


########################################################################
class ShowUI(QMainWindow):
    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()
        self.main = QUiLoader().load('window.ui', self)


if __name__ == "__main__":
    app = QApplication()

    apply_stylesheet(app, theme='dark_cyan.xml')

    frame = ShowUI()
    frame.main.show()

    app.exec_()
