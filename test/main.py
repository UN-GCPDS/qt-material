import os
import sys
import logging
from multiprocessing import freeze_support
import psutil
import signal

if '--pyside2' in sys.argv:
    from PySide2.QtWidgets import QApplication, QMainWindow, QColorDialog
    from PySide2.QtCore import QTimer, Qt, QCoreApplication
    from PySide2.QtGui import QColor
    from PySide2.QtUiTools import QUiLoader

elif '--pyside6' in sys.argv:
    from PySide6.QtWidgets import QApplication, QMainWindow, QColorDialog
    from PySide6.QtCore import QTimer, Qt, QCoreApplication
    from PySide6.QtGui import QColor
    from PySide6.QtUiTools import QUiLoader

elif '--pyqt5' in sys.argv:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog
    from PyQt5.QtCore import QTimer, Qt, QCoreApplication
    from PyQt5.QtGui import QColor
    from PyQt5 import uic, QtWebEngineWidgets


from qt_material import apply_stylesheet, QtStyleSwitcher

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
# app.lastWindowClosed.connect(kill_childs)
app.lastWindowClosed.connect(lambda: app.quit())

app.setStyle('Fusion')  # For better looking

extra = {'danger': '#dc3545',
         'warning': '#ffc107',
         'success': '#17a2b8',
         }


########################################################################
class RuntimeStylesheets(QMainWindow, QtStyleSwitcher):
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super().__init__()

        # Extra stylesheets

        self.colors = ['primaryColor',
                       'primaryLightColor',
                       'secondaryColor',
                       'secondaryLightColor',
                       'secondaryDarkColor',
                       'primaryTextColor',
                       'secondaryTextColor']

        self.custom_colors = {v: os.environ[f'PYSIDEMATERIAL_{v.upper()}'] for v in self.colors}

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
        self.update_buttons()
        self.set_style_switcher(self.main, self.main.menuStyles, extra, self.update_buttons)

        self.main.checkBox_ligh_theme.clicked.connect(self.update_theme)

        for color in self.colors:
            button = getattr(self.main, f'pushButton_{color}')
            button.clicked.connect(self.set_color(color))

        self.main.dockWidget_theme.setFloating(True)

    # ----------------------------------------------------------------------
    def set_color(self, button_):
        """"""
        def iner():
            initial = self.get_color(self.custom_colors[button_])
            color_dialog = QColorDialog(parent=self.main)
            color_dialog.setCurrentColor(initial)
            done = color_dialog.exec_()
            color_ = color_dialog.currentColor()

            if done and color_.isValid():
                color = '#' + ''.join([hex(v)[2:].ljust(2, '0') for v in color_.toTuple()[:3]])
                self.custom_colors[button_] = color
                self.update_theme()

        return iner

    # ----------------------------------------------------------------------
    def custom_styles(self):
        """"""
        for i in range(self.main.toolBar_vertical.layout().count()):
            tool_button = self.main.toolBar_vertical.layout().itemAt(i).widget()
            tool_button.setMaximumWidth(150)
            tool_button.setMinimumWidth(150)

    # ----------------------------------------------------------------------
    def update_theme(self, event=None):
        """"""
        with open('my_theme.xml', 'w') as file:
            file.write("""
            <resources>
                <color name="primaryColor">{primaryColor}</color>
                <color name="primaryLightColor">{primaryLightColor}</color>
                <color name="secondaryColor">{secondaryColor}</color>
                <color name="secondaryLightColor">{secondaryLightColor}</color>
                <color name="secondaryDarkColor">{secondaryDarkColor}</color>
                <color name="primaryTextColor">{primaryTextColor}</color>
                <color name="secondaryTextColor">{secondaryTextColor}</color>
              </resources>
            """.format(**self.custom_colors))

        light = self.main.checkBox_ligh_theme.isChecked()
        self.apply_stylesheet(self.main, 'my_theme.xml', invert_secondary=light, extra=extra, callable_=self.update_buttons)

    # ----------------------------------------------------------------------
    def update_buttons(self):
        """"""
        theme = {color_: os.environ[f'PYSIDEMATERIAL_{color_.upper()}'] for color_ in self.colors}

        if 'light' in os.environ['PYSIDEMATERIAL_THEME']:
            self.main.checkBox_ligh_theme.setChecked(True)
        elif 'dark' in os.environ['PYSIDEMATERIAL_THEME']:
            self.main.checkBox_ligh_theme.setChecked(False)

        if self.main.checkBox_ligh_theme.isChecked():
            theme['secondaryColor'], theme['secondaryLightColor'], theme['secondaryDarkColor'] = theme[
                'secondaryColor'], theme['secondaryDarkColor'], theme['secondaryLightColor']
            # theme['primaryTextColor'] = theme['secondaryTextColor']

        for color_ in self.colors:
            button = getattr(self.main, f'pushButton_{color_}')

            color = theme[color_]

            if self.get_color(color).getHsv()[2] < 128:
                text_color = '#ffffff'
            else:
                text_color = '#000000'

            button.setStyleSheet(f"""
            *{{
            background-color: {color};
            color: {text_color};
            border: none;
            }}""")

            self.custom_colors[color_] = color

    # ----------------------------------------------------------------------
    def get_color(self, color):
        """"""
        return QColor(*[int(color[s:s + 2], 16) for s in range(1, 6, 2)])


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
        # theme = 'default_light'

    # Set theme on in itialization
    apply_stylesheet(app, theme + '.xml',
                     invert_secondary=('light' in theme and 'dark' not in theme),
                     extra=extra)
    # QIcon.setThemeName("breeze-dark")

    frame = RuntimeStylesheets()
    frame.main.show()

    app.exec_()








