from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QFontDatabase
from qt_material import QtStyleTools


########################################################################
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()
        self.main = QUiLoader().load('main_window.ui', self)

        self.main.pushButton.clicked.connect(lambda: self.apply_stylesheet(self.main, 'dark_teal.xml'))
        self.main.pushButton_2.clicked.connect(lambda: self.apply_stylesheet(self.main, 'light_red.xml', extra={'font_family': 'mono', }))
        self.main.pushButton_3.clicked.connect(lambda: self.apply_stylesheet(self.main, 'light_blue.xml', extra={'font_family': 'Raleway', }))


if __name__ == "__main__":
    app = QApplication()

    # Local file
    QFontDatabase.addApplicationFont('Raleway-Regular.ttf')

    frame = RuntimeStylesheets()
    frame.main.show()

    app.exec_()

