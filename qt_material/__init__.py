import os
import sys
from textwrap import wrap
import logging
from xml.etree import ElementTree


if 'PySide2' in sys.modules:
    from PySide2.QtGui import QFontDatabase, QColor, QGuiApplication, QPalette
    from PySide2.QtWidgets import QAction, QColorDialog
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import Qt
    _resource = os.path.join('resources', 'resource_pyside2_rc.py')

elif 'PySide6' in sys.modules:
    from PySide6.QtGui import QFontDatabase, QAction, QColor, QGuiApplication, QPalette
    from PySide6.QtWidgets import QColorDialog
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import Qt
    _resource = os.path.join('resources', 'resource_pyside6_rc.py')

elif 'PyQt5' in sys.modules:
    from PyQt5.QtGui import QFontDatabase, QColor, QGuiApplication, QPalette
    from PyQt5.QtWidgets import QAction, QColorDialog
    from PyQt5.QtCore import Qt
    from PyQt5 import uic
    _resource = os.path.join('resources', 'resource_pyqt5_rc.py')
else:
    logging.warning("qt_material must be imported after PySide or PyQt!")

import jinja2

template = 'material.css.template'


# ----------------------------------------------------------------------
def build_stylesheet(theme='', invert_secondary=False, resources=[], extra={}):
    """"""
    theme = get_theme(theme, invert_secondary)
    if theme is None:
        return None

    set_icons_theme(theme)

    loader = jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(os.path.abspath(__file__))))
    env = jinja2.Environment(autoescape=True, loader=loader)

    theme['icon'] = None

    env.filters['opacity'] = opacity
    # env.filters['load'] = load

    stylesheet = env.get_template(template)

    theme.setdefault('font_family', 'Roboto')
    theme.setdefault('danger', '#dc3545')
    theme.setdefault('warning', '#ffc107')
    theme.setdefault('success', '#17a2b8')

    theme.update(extra)

    default_palette = QGuiApplication.palette()
    default_palette.setColor(QPalette.PlaceholderText, QColor(*[int(theme['primaryColor'][i:i + 2], 16) for i in range(1, 6, 2)] + [92]))
    QGuiApplication.setPalette(default_palette)

    return stylesheet.render(**theme)


# ----------------------------------------------------------------------
def get_theme(theme_name, invert_secondary=False):
    if theme_name in ['default.xml', 'default_dark.xml', 'default', 'default_dark']:
        theme = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'themes', 'dark_teal.xml')
    elif theme_name in ['default_light.xml', 'default_light']:
        invert_secondary = True
        theme = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'themes', 'light_blue.xml')
    elif not os.path.exists(theme_name):
        theme = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'themes', theme_name)
    else:
        theme = theme_name

    if not os.path.exists(theme):
        logging.warning(f"{theme} not exist!")
        return None

    tree = ElementTree.parse(theme)
    theme = {child.attrib['name']: child.text for child in tree.getroot()}

    for k in theme:
        os.environ[str(k)] = theme[k]

    if invert_secondary:
        theme['secondaryColor'], theme['secondaryLightColor'], theme['secondaryDarkColor'] = theme[
            'secondaryColor'], theme['secondaryDarkColor'], theme['secondaryLightColor']

    for color in ['primaryColor',
                  'primaryLightColor',
                  'secondaryColor',
                  'secondaryLightColor',
                  'secondaryDarkColor',
                  'primaryTextColor',
                  'secondaryTextColor']:
        os.environ[f'QTMATERIAL_{color.upper()}'] = theme[color]
    os.environ['QTMATERIAL_THEME'] = theme_name

    return theme


# ----------------------------------------------------------------------
def add_fonts():
    """"""
    fonts_path = os.path.join(os.path.dirname(__file__), 'fonts')

    for font in ['roboto']:
        for font in filter(lambda s: s.endswith('.ttf'), os.listdir(os.path.join(fonts_path, font))):
            QFontDatabase.addApplicationFont(os.path.join(fonts_path, font))


# ----------------------------------------------------------------------
def apply_stylesheet(app, theme='', style='Fusion', save_as=None, invert_secondary=False, resources=[], extra={}):
    """"""
    add_fonts()

    if style:
        try:
            app.setStyle(style)
        except:
            pass
    stylesheet = build_stylesheet(theme, invert_secondary, resources, extra)
    if stylesheet is None:
        return

    if save_as:
        with open(save_as, 'w') as file:
            file.writelines(stylesheet)

    return app.setStyleSheet(stylesheet)


# ----------------------------------------------------------------------
def opacity(theme, value=0.5):
    """"""
    r, g, b = theme[1:][0:2], theme[1:][2:4], theme[1:][4:]
    r, g, b = int(r, 16), int(g, 16), int(b, 16)

    return f'rgba({r}, {g}, {b}, {value})'


# ----------------------------------------------------------------------
def str16b(c):
    """"""
    return '\\x' + '\\x'.join(wrap(c.encode().hex(), 2))


# ----------------------------------------------------------------------
def set_icons_theme(theme, resource=None, output=None):
    """"""
    try:
        theme = get_theme(theme)
    except:
        pass

    if resource is None:
        resource = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), _resource)

    with open(resource, 'r') as file:
        content = file.read()

        replaces = (
            ["#0000ff", 'primaryColor'],
            ["#ff0000", 'secondaryLightColor'],)

        for color, replace in replaces:
            if 'PySide2' in sys.modules or 'PySide6' in sys.modules:
                colors = [
                    color] + [''.join(list(color)[:i] + ['\\\n'] + list(color)[i:]) for i in range(1, 7)]
                for c in colors:
                    content = content.replace(c, theme[replace])
            elif 'PyQt5' in sys.modules:
                colors = [str16b(color)] + [str16b(color)[:i] + '\\\n' + str16b(color)[i:] for i in range(4, 28, 4)]
                for c in colors:
                    content = content.replace(c, str16b(theme[replace]))

    if output:
        with open(output, 'w') as file:
            file.write(content)
        return

    try:
        qCleanupResources()  # this method is created after the first call to resource_rc
    except:
        pass

    # This is like import resource_rc, load new resources with icons
    exec(content, globals())


# ----------------------------------------------------------------------
def list_themes():
    """"""
    themes = os.listdir(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'themes'))
    themes = filter(lambda a: a.endswith('xml'), themes)
    return sorted(list(themes))


########################################################################
class QtStyleTools:
    """"""
    extra_colors = {}

    # ----------------------------------------------------------------------
    def set_extra_colors(self, extra):
        """"""
        self.extra_colors = extra

    # ----------------------------------------------------------------------
    def add_menu_theme(self, parent, menu):
        """"""
        for theme in ['default'] + list_themes():
            action = QAction(parent)
            action.setText(theme)
            action.triggered.connect(self._wrapper(parent, theme, self.extra_colors, self.update_buttons))
            menu.addAction(action)

    # ----------------------------------------------------------------------
    def _wrapper(self, parent, theme, extra, callable_):
        """"""
        def iner():
            self._apply_theme(parent, theme, extra, callable_)
        return iner

    # ----------------------------------------------------------------------
    def _apply_theme(self, parent, theme, extra={}, callable_=None):
        """"""
        self.apply_stylesheet(parent, theme=theme, invert_secondary=theme.startswith(
            'light'), extra=extra, callable_=callable_)

    # ----------------------------------------------------------------------
    def apply_stylesheet(self, parent, theme, invert_secondary=False, extra={}, callable_=None):
        """"""
        if theme == 'default':
            parent.setStyleSheet('')
            return
        apply_stylesheet(parent, theme=theme, invert_secondary=invert_secondary, extra=extra)

        if callable_:
            callable_()

    # ----------------------------------------------------------------------
    def update_buttons(self):
        """"""
        if not hasattr(self, 'colors'):
            return

        theme = {color_: os.environ[f'QTMATERIAL_{color_.upper()}'] for color_ in self.colors}

        if 'light' in os.environ['QTMATERIAL_THEME']:
            self.dock_theme.checkBox_ligh_theme.setChecked(True)
        elif 'dark' in os.environ['QTMATERIAL_THEME']:
            self.dock_theme.checkBox_ligh_theme.setChecked(False)

        if self.dock_theme.checkBox_ligh_theme.isChecked():
            theme['secondaryColor'], theme['secondaryLightColor'], theme['secondaryDarkColor'] = theme[
                'secondaryColor'], theme['secondaryDarkColor'], theme['secondaryLightColor']

        for color_ in self.colors:
            button = getattr(self.dock_theme, f'pushButton_{color_}')

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

    # ----------------------------------------------------------------------
    def update_theme(self, parent):
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
        light = self.dock_theme.checkBox_ligh_theme.isChecked()
        self.apply_stylesheet(parent, 'my_theme.xml', invert_secondary=light, extra=self.extra_colors, callable_=self.update_buttons)

    # ----------------------------------------------------------------------
    def set_color(self, parent, button_):
        """"""
        def iner():
            initial = self.get_color(self.custom_colors[button_])
            color_dialog = QColorDialog(parent=parent)
            color_dialog.setCurrentColor(initial)
            done = color_dialog.exec_()
            color_ = color_dialog.currentColor()

            if done and color_.isValid():
                color = '#' + ''.join([hex(v)[2:].ljust(2, '0') for v in color_.toTuple()[:3]])
                self.custom_colors[button_] = color
                self.update_theme(parent)

        return iner

    # ----------------------------------------------------------------------
    def show_dock_theme(self, parent):
        """"""
        self.colors = ['primaryColor',
                       'primaryLightColor',
                       'secondaryColor',
                       'secondaryLightColor',
                       'secondaryDarkColor',
                       'primaryTextColor',
                       'secondaryTextColor']

        self.custom_colors = {v: os.environ[f'QTMATERIAL_{v.upper()}'] for v in self.colors}

        if 'PySide2' in sys.modules or 'PySide6' in sys.modules:
            self.dock_theme = QUiLoader().load(os.path.join(os.path.dirname(__file__), 'dock_theme.ui'))
        elif 'PyQt5' in sys.modules:
            self.dock_theme = uic.loadUi(os.path.join(os.path.dirname(__file__), 'dock_theme.ui'))

        parent.addDockWidget(Qt.LeftDockWidgetArea, self.dock_theme)
        self.dock_theme.setFloating(True)

        self.update_buttons()
        self.dock_theme.checkBox_ligh_theme.clicked.connect(lambda: self.update_theme(self.main))

        for color in self.colors:
            button = getattr(self.dock_theme, f'pushButton_{color}')
            button.clicked.connect(self.set_color(parent, color))

