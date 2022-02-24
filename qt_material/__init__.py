import os
import sys
import logging
import base64
from pathlib import Path
import platform
from xml.dom.minidom import parse

from qt_material.resources import ResourseGenerator, RESOURCES_PATH
GUI = True

if 'PySide2' in sys.modules:
    from PySide2.QtGui import QFontDatabase, QColor, QGuiApplication, QPalette
    from PySide2.QtWidgets import QAction, QColorDialog, QActionGroup
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import Qt, QDir

elif 'PySide6' in sys.modules:
    from PySide6.QtGui import QFontDatabase, QAction, QColor, QGuiApplication, QPalette, QActionGroup
    from PySide6.QtWidgets import QColorDialog
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import Qt, QDir

elif 'PyQt5' in sys.modules:
    from PyQt5.QtGui import QFontDatabase, QColor, QGuiApplication, QPalette
    from PyQt5.QtWidgets import QAction, QColorDialog, QActionGroup
    from PyQt5.QtCore import Qt, QDir
    from PyQt5 import uic

elif 'PyQt6' in sys.modules:
    from PyQt6.QtGui import QFontDatabase, QColor, QGuiApplication, QPalette, QAction, QActionGroup
    from PyQt6.QtWidgets import QColorDialog
    from PyQt6.QtCore import Qt, QDir
    from PyQt6 import uic
else:
    GUI = False
    logging.warning("qt_material must be imported after PySide or PyQt!")

import jinja2

TEMPLATE_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'material.css.template')


# ----------------------------------------------------------------------
def export_theme(theme='', qss=None, rcc=None, invert_secondary=False, extra={}, output='theme', prefix='icon:/'):
    """"""
    if not os.path.isabs(output) and not output.startswith('.'):
            output = f'.{output}'

    stylesheet = build_stylesheet(
        theme, invert_secondary, extra, output, export=True)

    if output.startswith('.'):
        output = output[1:]

    with open(qss, 'w') as file:
        file.writelines(stylesheet.replace('icon:/', prefix))

    if rcc:

        with open(rcc, 'w') as file:
            file.write('<RCC>\n')
            file.write(f'  <qresource prefix="{prefix[:-2]}">\n')

            for subfolder in ['disabled', 'primary']:
                files = os.listdir(os.path.join(
                    os.path.abspath(output), subfolder))
                files = filter(lambda s: s.endswith('svg'), files)
                for filename in files:
                    file.write(
                        f'    <file>{output}/{subfolder}/{filename}</file>\n')

            file.write('  </qresource>\n')

            file.write(f'  <qresource prefix="file">\n')
            if qss:
                file.write(f'    <file>{qss}</file>\n')
            file.write('  </qresource>\n')

            file.write('</RCC>\n')


# ----------------------------------------------------------------------
def build_stylesheet(theme='', invert_secondary=False, extra={}, parent='theme', template=TEMPLATE_FILE, export=False):
    """"""

    if not export:
        try:
            add_fonts()
        except Exception as e:
            logging.warning(e)

    theme = get_theme(theme, invert_secondary)
    if theme is None:
        return None

    set_icons_theme(theme, parent=parent)

    # Render custom template
    if os.path.exists(template):
        parent, template = os.path.split(template)
        loader = jinja2.FileSystemLoader(parent)
        env = jinja2.Environment(autoescape=False, loader=loader)
        env.filters['opacity'] = opacity
        env.filters['density'] = density
        stylesheet = env.get_template(template)
    else:
        env = jinja2.Environment(autoescape=False, loader=jinja2.BaseLoader)
        env.filters['opacity'] = opacity
        env.filters['density'] = density
        stylesheet.from_string(template)

    theme.setdefault('icon', None)
    theme.setdefault('font_family', 'Roboto')
    theme.setdefault('danger', '#dc3545')
    theme.setdefault('warning', '#ffc107')
    theme.setdefault('success', '#17a2b8')
    theme.setdefault('density_scale', '0')
    theme.setdefault('button_shape', 'default')

    theme.update(extra)

    if GUI:
        default_palette = QGuiApplication.palette()
        color = QColor(*[int(theme['primaryColor'][i:i + 2], 16)
                         for i in range(1, 6, 2)] + [92])

        try:
            if hasattr(QPalette, 'PlaceholderText'):  # pyqt5, pyside2, pyside6
                default_palette.setColor(QPalette.PlaceholderText, color)
            else:  # pyqt6
                default_palette.setColor(QPalette.ColorRole.Text, color)
            QGuiApplication.setPalette(default_palette)

        except:  # pyside6  & snake_case, true_property
            default_palette.set_color(QPalette.ColorRole.Text, color)
            QGuiApplication.set_palette(default_palette)

    environ = {

        'linux': platform.system() == 'Linux',
        'windows': platform.system() == 'Windows',
        'darwin': platform.system() == 'Darwin',

        'pyqt5': 'PyQt5' in sys.modules,
        'pyqt6': 'PyQt6' in sys.modules,
        'pyside2': 'PySide2' in sys.modules,
        'pyside6': 'PySide6' in sys.modules,
    }

    environ.update(theme)
    return stylesheet.render(environ)


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

    document = parse(theme)
    theme = {child.getAttribute(
        'name'): child.firstChild.nodeValue for child in document.getElementsByTagName('color')}

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

    for font_dir in ['roboto']:
        for font in filter(lambda s: s.endswith('.ttf'), os.listdir(os.path.join(fonts_path, font_dir))):
            try:
                QFontDatabase.addApplicationFont(
                    os.path.join(fonts_path, font_dir, font))
            except:  # snake_case, true_property
                QFontDatabase.add_application_font(
                    os.path.join(fonts_path, font_dir, font))


# ----------------------------------------------------------------------
def apply_stylesheet(app, theme='', style=None, save_as=None, invert_secondary=False, extra={}, parent='theme'):
    """"""
    if style:
        try:
            try:
                app.setStyle(style)
            except:  # snake_case, true_property
                app.style = style
        except:
            logging.error(f"The style '{style}' does not exist.")
            pass

    stylesheet = build_stylesheet(
        theme, invert_secondary, extra, parent)
    if stylesheet is None:
        return

    if save_as:
        with open(save_as, 'w') as file:
            file.writelines(stylesheet)

    try:
        app.setStyleSheet(stylesheet)
    except:
        app.style_sheet = stylesheet


# ----------------------------------------------------------------------
def opacity(theme, value=0.5):
    """"""
    r, g, b = theme[1:][0:2], theme[1:][2:4], theme[1:][4:]
    r, g, b = int(r, 16), int(g, 16), int(b, 16)

    return f'rgba({r}, {g}, {b}, {value})'


# ----------------------------------------------------------------------
def density(value, density_scale, border=0, scale=1, density_interval=4):
    """"""
    # https://material.io/develop/web/supporting/density
    if isinstance(value, str) and value.startswith('@'):
        return value[1:] * scale

    if value == 'unset':
        return 'unset'

    if isinstance(value, str):
        value = float(value.replace('px', ''))

    density = (value + (density_interval * int(density_scale)) -
               (border * 2)) * scale

    if density < 0:
        density = 0
    return density


# ----------------------------------------------------------------------
def set_icons_theme(theme, parent='theme'):
    """"""
    source = os.path.join(os.path.dirname(__file__), 'resources', 'source')
    resources = ResourseGenerator(primary=theme['primaryColor'], secondary=theme['secondaryColor'],
                                  disabled=theme['secondaryLightColor'], source=source, parent=parent)
    resources.generate()

    if GUI:
        try:
            QDir.addSearchPath('icon', resources.index)
            QDir.addSearchPath('qt_material', os.path.join(
                os.path.dirname(__file__), 'resources'))
        except:  # snake_case, true_property
            QDir.add_search_path('icon', resources.index)
            QDir.add_search_path('qt_material', os.path.join(
                os.path.dirname(__file__), 'resources'))


# ----------------------------------------------------------------------
def list_themes():
    """"""
    themes = os.listdir(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'themes'))
    themes = filter(lambda a: a.endswith('xml'), themes)
    return sorted(list(themes))


# ----------------------------------------------------------------------
def deprecated(replace):
    """"""
    # ----------------------------------------------------------------------
    def wrap1(fn):
        # ----------------------------------------------------------------------
        def wrap2(*args, **kwargs):
            logging.warning(
                f'This function is deprecated, please use "{replace}" instead.')
            fn(*args, **kwargs)
        return wrap2

    return wrap1


########################################################################
class QtStyleTools:
    """"""
    extra_values = {}

    # ----------------------------------------------------------------------
    @deprecated('set_extra')
    def set_extra_colors(self, extra):
        """"""
        self.extra_values = extra

    # ----------------------------------------------------------------------
    def set_extra(self, extra):
        """"""
        self.extra_values = extra

    # ----------------------------------------------------------------------
    def add_menu_theme(self, parent, menu):
        """"""
        self.menu_theme_ = menu
        action_group = QActionGroup(menu)
        try:
            action_group.setExclusive(True)
        except:
            action_group.exclusive = True

        for i, theme in enumerate(['default'] + list_themes()):
            action = QAction(parent)
            # action.triggered.connect(self._wrapper(parent, theme, self.extra_values, self.update_buttons))
            action.triggered.connect(lambda: self.update_theme_event(parent))
            try:
                action.setText(theme)
                action.setCheckable(True)
                action.setChecked(not bool(i))
                action.setActionGroup(action_group)
                menu.addAction(action)
                action_group.addAction(action)
            except:  # snake_case, true_property
                action.text = theme
                action.checkable = True
                action.checked = not bool(i)
                action.action_group = action_group
                menu.add_action(action)
                action_group.add_action(action)

    # ----------------------------------------------------------------------
    def add_menu_density(self, parent, menu):
        """"""
        self.menu_density_ = menu
        action_group = QActionGroup(menu)

        try:
            action_group.setExclusive(True)
        except:
            action_group.exclusive = True

        for density in map(str, range(-3, 4)):
            action = QAction(parent)
            # action.triggered.connect(self._wrapper(parent, density, self.extra_values, self.update_buttons))
            action.triggered.connect(lambda: self.update_theme_event(parent))
            try:
                action.setText(density)
                action.setCheckable(True)
                action.setChecked(density == '0')
                action.setActionGroup(action_group)
                menu.addAction(action)
                action_group.addAction(action)
            except:  # snake_case, true_property
                action.text = density
                action.checkable = True
                action.checked = density == '0'
                action.action_group = action_group
                menu.add_action(action)
                action_group.add_action(action)

        # menu.add_action(action_group)

    # # ----------------------------------------------------------------------
    # def _wrapper(self, parent, theme, extra, callable_):
        # """"""
        # def iner():
            # self._apply_theme(parent, theme, extra, callable_)
        # return iner

    # # ----------------------------------------------------------------------
    # def _apply_theme(self, parent, theme, extra={}, callable_=None):
        # """"""
        # self.apply_stylesheet(parent, theme=theme, invert_secondary=theme.startswith(
            # 'light'), extra=extra, callable_=callable_)

    # ----------------------------------------------------------------------

    def apply_stylesheet(self, parent, theme, invert_secondary=False, extra={}, callable_=None):
        """"""
        if theme == 'default':
            parent.setStyleSheet('')
            return
        apply_stylesheet(parent, theme=theme,
                         invert_secondary=invert_secondary, extra=extra)

        if callable_:
            callable_()

    # ----------------------------------------------------------------------
    def update_theme_event(self, parent):
        """"""
        try:
            density = [action.text() for action in self.menu_density_.actions(
            ) if action.isChecked()][0]
            theme = [action.text() for action in self.menu_theme_.actions()
                     if action.isChecked()][0]
        except:
            density = [
                action.text for action in self.menu_density_.actions() if action.checked][0]
            theme = [action.text for action in self.menu_theme_.actions()
                     if action.checked][0]

        self.extra_values['density_scale'] = density

        self.apply_stylesheet(parent, theme=theme, invert_secondary=theme.startswith(
            'light'), extra=self.extra_values, callable_=self.update_buttons)

    # ----------------------------------------------------------------------
    def update_buttons(self):
        """"""
        if not hasattr(self, 'colors'):
            return

        theme = {color_: os.environ[f'QTMATERIAL_{color_.upper()}']
                 for color_ in self.colors}

        if 'light' in os.environ['QTMATERIAL_THEME']:
            self.dock_theme.checkBox_ligh_theme.setChecked(True)
        elif 'dark' in os.environ['QTMATERIAL_THEME']:
            self.dock_theme.checkBox_ligh_theme.setChecked(False)

        try:
            if self.dock_theme.checkBox_ligh_theme.isChecked():
                theme['secondaryColor'], theme['secondaryLightColor'], theme['secondaryDarkColor'] = theme[
                    'secondaryColor'], theme['secondaryDarkColor'], theme['secondaryLightColor']
        except:  # snake_case, true_property
            if self.dock_theme.checkBox_ligh_theme.checked:
                theme['secondaryColor'], theme['secondaryLightColor'], theme['secondaryDarkColor'] = theme[
                    'secondaryColor'], theme['secondaryDarkColor'], theme['secondaryLightColor']

        for color_ in self.colors:
            button = getattr(self.dock_theme, f'pushButton_{color_}')

            color = theme[color_]

            try:
                if self.get_color(color).getHsv()[2] < 128:
                    text_color = '#ffffff'
                else:
                    text_color = '#000000'
            except:  # snake_case, true_property
                if self.get_color(color).get_hsv()[2] < 128:
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
        try:
            light = self.dock_theme.checkBox_ligh_theme.isChecked()
        except:  # snake_case, true_property
            light = self.dock_theme.checkBox_ligh_theme.checked

        self.apply_stylesheet(parent, 'my_theme.xml', invert_secondary=light,
                              extra=self.extra_values, callable_=self.update_buttons)

    # ----------------------------------------------------------------------
    def set_color(self, parent, button_):
        """"""
        def iner():
            initial = self.get_color(self.custom_colors[button_])
            color_dialog = QColorDialog(parent=parent)
            try:
                color_dialog.setCurrentColor(initial)
            except:  # snake_case, true_property
                color_dialog.current_color = initial
            done = color_dialog.exec_()

            try:
                color_ = color_dialog.currentColor()
            except:  # snake_case, true_property
                color_ = color_dialog.current_color

            try:
                if done and color_.isValid():
                    rgb_255 = [color_.red(), color_.green(), color_.blue()]
                    color = '#' + ''.join([hex(v)[2:].ljust(2, '0')
                                           for v in rgb_255])
                    self.custom_colors[button_] = color
                    self.update_theme(parent)
            except:  # snake_case, true_property
                if done and color_.is_valid():
                    rgb_255 = [color_.red(), color_.green(), color_.blue()]
                    color = '#' + ''.join([hex(v)[2:].ljust(2, '0')
                                           for v in rgb_255])
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

        self.custom_colors = {
            v: os.environ[f'QTMATERIAL_{v.upper()}'] for v in self.colors}

        if 'PySide2' in sys.modules or 'PySide6' in sys.modules:
            self.dock_theme = QUiLoader().load(os.path.join(
                os.path.dirname(__file__), 'dock_theme.ui'))
        elif 'PyQt5' in sys.modules or 'PyQt6' in sys.modules:
            self.dock_theme = uic.loadUi(os.path.join(
                os.path.dirname(__file__), 'dock_theme.ui'))

        try:
            parent.addDockWidget(
                Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_theme)
            self.dock_theme.setFloating(True)
        except:  # snake_case, true_property
            parent.add_dock_widget(
                Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_theme)
            self.dock_theme.floating = True

        self.update_buttons()
        self.dock_theme.checkBox_ligh_theme.clicked.connect(
            lambda: self.update_theme(self.main))

        for color in self.colors:
            button = getattr(self.dock_theme, f'pushButton_{color}')
            button.clicked.connect(self.set_color(parent, color))


# ----------------------------------------------------------------------
def get_hook_dirs():
    package_folder = Path(__file__).parent
    return [str(package_folder.absolute())]
