from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from qt_material import QtStyleTools


########################################################################
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()
        self.main = QUiLoader().load('main_window.ui', self)

        self.add_menu_theme(self.main, self.main.menuStyles)


if __name__ == "__main__":
    app = QApplication()
    frame = RuntimeStylesheets()
    frame.main.show()
    app.exec_()

