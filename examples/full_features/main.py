import os
import sys
import logging
from multiprocessing import freeze_support
# import psutil
# import signal
# import importlib.resources

if '--pyside2' in sys.argv:
    from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
    from PySide2.QtCore import QTimer, Qt, QCoreApplication
    from PySide2.QtGui import QIcon
    from PySide2.QtUiTools import QUiLoader

elif '--pyside6' in sys.argv:
    from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
    from PySide6.QtCore import QTimer, Qt, QCoreApplication
    from PySide6.QtGui import QIcon, QPixmap
    from PySide6.QtUiTools import QUiLoader
    from __feature__ import snake_case, true_property

elif '--pyqt5' in sys.argv:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
    from PyQt5.QtCore import QTimer, Qt, QCoreApplication
    from PyQt5 import uic, QtWebEngineWidgets
    from PyQt5.QtGui import QIcon

elif '--pyqt6' in sys.argv:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
    from PyQt6.QtCore import QTimer, Qt, QCoreApplication
    from PyQt6.QtGui import QIcon
    from PyQt6 import uic, QtWebEngineWidgets

from qt_material import apply_stylesheet, QtStyleTools, density

if hasattr(Qt, 'AA_ShareOpenGLContexts'):
    try:
        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    except:
        QCoreApplication.set_attribute(Qt.AA_ShareOpenGLContexts)
else:
    print("'Qt' object has no attribute 'AA_ShareOpenGLContexts'")

app = QApplication([])
freeze_support()
try:
    app.processEvents()
    app.setQuitOnLastWindowClosed(False)
    app.lastWindowClosed.connect(app.quit)
except:
    app.process_events()
    app.quit_on_last_window_closed = False
    app.lastWindowClosed.connect(app.quit)


# Extra stylesheets
extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'Roboto',

    # Density
    'density_scale': '0',

    # Button Shape
    'button_shape': 'default',
}


########################################################################
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super().__init__()

        if '--pyside2' in sys.argv:
            self.main = QUiLoader().load('main_window.ui', self)
            wt = 'PySide2'

        elif'--pyside6' in sys.argv:
            self.main = QUiLoader().load('main_window.ui', self)
            wt = 'PySide6'

        elif '--pyqt5' in sys.argv:
            self.main = uic.loadUi('main_window.ui', self)
            wt = 'PyQt5'

        elif '--pyqt6' in sys.argv:
            self.main = uic.loadUi('main_window.ui', self)
            wt = 'PyQt6'

        else:
            logging.error(
                'must include --pyside2, --pyside6 or --pyqt5 in args!')
            sys.exit()

        try:
            self.main.setWindowTitle(f'{self.main.windowTitle()} - {wt}')
        except:
            self.main.window_title = f'{self.main.window_title} - {wt}'

        self.custom_styles()

        self.set_extra(extra)
        self.add_menu_theme(self.main, self.main.menuStyles)
        self.add_menu_density(self.main, self.main.menuDensity)
        self.show_dock_theme(self.main)

        logo = QIcon("qt_material:/logo/logo.svg")
        logo_frame = QIcon("qt_material:/logo/logo_frame.svg")

        try:
            self.main.setWindowIcon(logo)
            self.main.actionToolbar.setIcon(logo)
            [self.main.listWidget_2.item(i).setIcon(logo_frame)
             for i in range(self.main.listWidget_2.count())]
        except:
            self.main.window_icon = logo
            self.main.actionToolbar.icon = logo
            [setattr(self.main.listWidget_2.item(i), 'icon', logo_frame)
             for i in range(self.main.listWidget_2.count)]

        if hasattr(QFileDialog, 'getExistingDirectory'):
            self.main.pushButton_file_dialog.clicked.connect(
                lambda: QFileDialog.getOpenFileName(self.main))
            self.main.pushButton_folder_dialog.clicked.connect(
                lambda: QFileDialog.getExistingDirectory(self.main))
        else:
            self.main.pushButton_file_dialog.clicked.connect(
                lambda: QFileDialog.get_open_file_name(self.main))
            self.main.pushButton_folder_dialog.clicked.connect(
                lambda: QFileDialog.get_existing_directory(self.main))

        self.main.comboBox_8.style_sheet = """*{border-color: red; color: red}"""

    # ----------------------------------------------------------------------
    def custom_styles(self):
        """"""
        for i in range(self.main.toolBar_vertical.layout().count()):

            try:
                tool_button = self.main.toolBar_vertical.layout().itemAt(i).widget()
                tool_button.setMaximumWidth(150)
                tool_button.setMinimumWidth(150)
            except:
                tool_button = self.main.toolBar_vertical.layout().item_at(i).widget()
                tool_button.maximum_width = 150
                tool_button.minimum_width = 150
        try:
            for r in range(self.main.tableWidget.rowCount()):
                self.main.tableWidget.setRowHeight(r, 36)

            for r in range(self.main.tableWidget_2.rowCount()):
                self.main.tableWidget_2.setRowHeight(r, 36)

        except:
            for r in range(self.main.tableWidget.row_count):
                self.main.tableWidget.set_row_height(r, 36)

            for r in range(self.main.tableWidget_2.row_count):
                self.main.tableWidget_2.set_row_height(r, 36)


T0 = 1000

if __name__ == "__main__":

    # ----------------------------------------------------------------------
    def take_screenshot():
        pixmap = frame.main.grab()
        pixmap.save(os.path.join('screenshots', f'{theme}.png'))
        print(f'Saving {theme}')

    if len(sys.argv) > 2:
        theme = sys.argv[2]
        try:
            QTimer.singleShot(T0, take_screenshot)
            QTimer.singleShot(T0 * 2, app.closeAllWindows)
        except:
            QTimer.single_shot(T0, take_screenshot)
            QTimer.single_shot(T0 * 2, app.closeAllWindows)
    else:
        theme = 'default'

    # Set theme on in itialization
    apply_stylesheet(app, theme + '.xml',
                     invert_secondary=(
                         'light' in theme and 'dark' not in theme),
                     extra=extra)

    frame = RuntimeStylesheets()

    try:
        frame.main.showMaximized()
    except:
        frame.main.show_maximized()

    if hasattr(app, 'exec'):
        app.exec()
    else:
        app.exec_()








