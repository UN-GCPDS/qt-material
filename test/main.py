import os
import sys

from PySide2.QtWidgets import QApplication
from PySide2 import QtWidgets
from PySide2.QtCore import QTimer
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt, QCoreApplication

from pyside_material import apply_stylesheet, PySideStyleSwitcher

# To load window icon
from pyside_material.resources import logos_rc

QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

app = QApplication([])
app.processEvents()
app.setStyle('Fusion')  # For better looking


########################################################################
class RuntimeStylesheets(QtWidgets.QMainWindow, PySideStyleSwitcher):
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super().__init__()

        # Extra stylesheets
        self.extra = {'danger': '#dc3545',
                      'warning': '#ffc107',
                      'success': '#17a2b8',
                      }

        self.main = QUiLoader().load('main_window.ui', self)
        self.custom_styles()
        self.set_style_switcher(self.main, self.main.menuStyles, self.extra)

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
        theme = sys.argv[1]
        QTimer.singleShot(T0, take_screenshot)
        QTimer.singleShot(T0 * 2, app.closeAllWindows)
    except:
        theme = 'default'

    # Set theme on in itialization
    apply_stylesheet(app, theme + '.xml', light_secondary=('light' in theme))

    frame = RuntimeStylesheets()
    frame.main.show()

    app.exec_()








