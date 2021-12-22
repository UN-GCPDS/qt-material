from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from qt_material import apply_stylesheet


extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'monoespace',
    'font_size': '13px',
    'line_height': '13px',
}


########################################################################
class RuntimeStylesheets(QMainWindow):
    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()
        self.main = QUiLoader().load('main_window_extra.ui', self)

        self.main.pushButton_danger.setProperty('class', 'danger')
        self.main.pushButton_warning.setProperty('class', 'warning')
        self.main.pushButton_success.setProperty('class', 'success')


if __name__ == "__main__":
    app = QApplication()

    apply_stylesheet(app, theme='light_blue.xml', extra=extra)

    frame = RuntimeStylesheets()
    frame.main.show()
    app.exec_()

