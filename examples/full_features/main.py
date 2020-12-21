import os
import sys
import logging
from multiprocessing import freeze_support
import psutil
import signal

if '--pyside2' in sys.argv:
    from PySide2.QtWidgets import QApplication, QMainWindow
    from PySide2.QtCore import QTimer, Qt, QCoreApplication
    from PySide2.QtUiTools import QUiLoader

elif '--pyside6' in sys.argv:
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtCore import QTimer, Qt, QCoreApplication
    from PySide6.QtUiTools import QUiLoader

elif '--pyqt5' in sys.argv:
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from PyQt5.QtCore import QTimer, Qt, QCoreApplication
    from PyQt5 import uic, QtWebEngineWidgets


from qt_material import apply_stylesheet, QtStyleTools

# To load window icon
if 'PySide2' in sys.modules:
    from qt_material.resources import logos_pyside2_rc
elif 'PySide6' in sys.modules:
    from qt_material.resources import logos_pyside6_rc
elif 'Qt' in sys.modules:
    from qt_material.resources import logos_pyqt5_rc

freeze_support()
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

app = QApplication([])
app.processEvents()
app.setQuitOnLastWindowClosed(False)
app.lastWindowClosed.connect(lambda: app.quit())
app.setStyle('Fusion')  # For better looking

# Extra stylesheets
extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'Roboto',
}


########################################################################
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super().__init__()

        if '--pyside2' in sys.argv:
            self.main = QUiLoader().load('main_window.ui', self)
            self.main.setWindowTitle(f'{self.main.windowTitle()} - PySide2')

        elif'--pyside6' in sys.argv:
            self.main = QUiLoader().load('main_window.ui', self)
            self.main.setWindowTitle(f'{self.main.windowTitle()} - PySide6')

        elif '--pyqt5' in sys.argv:
            self.main = uic.loadUi('main_window.ui', self)
            self.main.setWindowTitle(f'{self.main.windowTitle()} - PyQt5')

        else:
            logging.error('must include --pyside2, --pyside6 or --pyqt5 in args!')
            sys.exit()
        self.custom_styles()

        self.set_extra_colors(extra)
        self.add_menu_theme(self.main, self.main.menuStyles)
        self.show_dock_theme(self.main)

    # ----------------------------------------------------------------------
    def custom_styles(self):
        """"""
        for i in range(self.main.toolBar_vertical.layout().count()):
            tool_button = self.main.toolBar_vertical.layout().itemAt(i).widget()
            tool_button.setMaximumWidth(150)
            tool_button.setMinimumWidth(150)


T0 = 1000

if __name__ == "__main__":

    # ----------------------------------------------------------------------
    def take_screenshot():
        pixmap = frame.main.grab()
        pixmap.save(os.path.join('screenshots', f'{theme}.png'))
        print(f'Saving {theme}')

    try:
        theme = sys.argv[2]
        QTimer.singleShot(T0, take_screenshot)
        QTimer.singleShot(T0 * 2, app.closeAllWindows)
    except:
        theme = 'default'

    # Set theme on in itialization
    apply_stylesheet(app, theme + '.xml',
                     invert_secondary=('light' in theme and 'dark' not in theme),
                     extra=extra)
    # QIcon.setThemeName("breeze-dark")

    # app.setStyleSheet("*{font-family: mono}")

    frame = RuntimeStylesheets()
    frame.main.show()

    app.exec_()








