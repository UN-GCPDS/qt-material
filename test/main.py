import os
import sys

from PySide2.QtWidgets import QApplication
from PySide2 import QtGui
from PySide2.QtCore import QTimer, QSize
from PySide2.QtUiTools import QUiLoader

from pyside_material import apply_stylesheet, build_stylesheet, list_themes


T0 = 1000

if __name__ == "__main__":

    app = QApplication([])

    # ----------------------------------------------------------------------
    def take_screenshot():
        """"""
        pixmap = QtGui.QPixmap.grabWindow(frame.winId())
        pixmap.save(os.path.join('screenshots', f'{theme}.png'))
        print(f'Saving {theme}')

    try:
        theme = sys.argv[1]
        QTimer.singleShot(T0, take_screenshot)
        QTimer.singleShot(T0 * 2, app.closeAllWindows)
    except:
        # theme = 'light_blue'
        theme = 'default'

    app.setStyleSheet("")


    extra = {'danger': '#dc3545',
             'warning': '#ffc107',
             'success': '#17a2b8',}
    apply_stylesheet(app, theme=f'{theme}.xml', light_secondary=theme.startswith('light'), save_as='material.qss', extra=extra)

    frame = QUiLoader().load('main_window.ui')
    frame.show()
    frame.statusbar.showMessage(f'Theme: {theme}.xml')

    for i in range(frame.toolBar_vertical.layout().count()):
        tool_button = frame.toolBar_vertical.layout().itemAt(i).widget()
        tool_button.setMaximumWidth(150)
        tool_button.setMinimumWidth(150)

    app.exec_()








