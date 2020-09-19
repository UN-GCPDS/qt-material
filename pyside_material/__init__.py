import os
import logging
from xml.etree import ElementTree

from PySide2.QtGui import QFontDatabase
import jinja2

template = 'material.css.template'
_resource = os.path.join('resources', 'resource_rc.py')

from PySide2.QtWidgets import QAction


# ----------------------------------------------------------------------
def build_stylesheet(theme='', light_secondary=False, resources=[], extra={}):
    """"""
    theme = get_theme(theme, light_secondary)
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

    theme.update(extra)

    return stylesheet.render(**theme)


# ----------------------------------------------------------------------
def get_theme(theme_name, light_secondary=False):
    if theme_name in ['default.xml', 'default_dark.xml', 'default', 'default_dark']:
        theme = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'themes', 'dark_teal.xml')
    elif theme_name in ['default_light.xml', 'default_light']:
        light_secondary = True
        theme = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'themes', 'light_blue.xml')
    else:
        theme = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'themes', theme_name)

    if not os.path.exists(theme):
        logging.warning(f"{theme} not exist!")
        return None

    tree = ElementTree.parse(theme)
    theme = {child.attrib['name']: child.text for child in tree.getroot()}

    for k in theme:
        os.environ[str(k)] = theme[k]

    if light_secondary:
        theme['secondaryColor'], theme['secondaryLightColor'], theme['secondaryDarkColor'] = theme[
            'secondaryColor'], theme['secondaryDarkColor'], theme['secondaryLightColor']
        theme['primaryTextColor'] = theme['secondaryTextColor']

    for color in ['primaryColor',
                  'primaryLightColor',
                  'primaryDarkColor',
                  'secondaryColor',
                  'secondaryLightColor',
                  'secondaryDarkColor',
                  'primaryTextColor',
                  'secondaryTextColor']:
        os.environ[f'PYSIDEMATERIAL_{color.upper()}'] = theme[color]
    os.environ['PYSIDEMATERIAL_THEME'] = theme_name

    return theme


# ----------------------------------------------------------------------
def add_fonts():
    """"""
    fonts_path = os.path.join(os.path.dirname(__file__), 'fonts')
    for font in os.listdir(fonts_path):
        QFontDatabase.addApplicationFont(os.path.join(fonts_path, font))


# ----------------------------------------------------------------------
def apply_stylesheet(app, theme='', style='Fusion', save_as=None, light_secondary=False, resources=[], extra={}):
    """"""
    add_fonts()

    if style:
        try:
            app.setStyle(style)
        except:
            pass
    stylesheet = build_stylesheet(theme, light_secondary, resources, extra)
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
            ["#ff0000", 'secondaryLightColor'],

        )

        for color, replace in replaces:
            colors = [
                color] + [''.join(list(color)[:i] + ['\\\n'] + list(color)[i:]) for i in range(1, 7)]
            for c in colors:
                content = content.replace(c, theme[replace])

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
class PySideStyleSwitcher:
    """"""
    # ----------------------------------------------------------------------

    def set_style_switcher(self, parent, menu, extra={}):
        """"""
        for theme in ['default'] + list_themes():
            action = QAction(parent)
            action.setText(theme)
            action.triggered.connect(self._wrapper(parent, theme, extra))
            menu.addAction(action)

    # ----------------------------------------------------------------------
    def _wrapper(self, parent, theme, extra):
        """"""
        def iner():
            self._apply_theme(parent, theme, extra)
        return iner

    # ----------------------------------------------------------------------
    def _apply_theme(self, parent, theme, extra):
        """"""
        if theme == 'default':
            parent.setStyleSheet('')
            return

        apply_stylesheet(parent, theme=theme, light_secondary=theme.startswith(
            'light'), extra=extra)
