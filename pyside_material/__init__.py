import os
import logging
from PySide2.QtGui import QFontDatabase

import jinja2
# from jinja2 import Template

from xml.etree import ElementTree


# from . import resource_rc

# with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resource_rc.py'), 'r') as file:
    # content = file.read()
    # # content = content.replace("#0000ff", theme['primaryColor'])
    # # content = content.replace("#ffff00", theme['secondaryColor'])
    # exec(content)


template = 'material.css.template'
_resource = os.path.join('resources', 'resource_rc.py')


# ----------------------------------------------------------------------
def build_stylesheet(theme='', light_secondary=False, resources=[], extra={}):
    """"""
    theme = get_theme(theme, light_secondary)
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
    if theme_name in ['default.xml', 'default_dark.xml']:
        default_theme = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'themes', 'dark_teal.xml')
    elif theme_name in ['default_light.xml']:
        light_secondary = True
        default_theme = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'themes', 'light_blue.xml')

    if not os.path.exists(theme_name):

        theme = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'themes', theme_name)
        if not os.path.exists(theme):

            if theme:
                logging.warning(
                    f"{theme} not exist, using {default_theme} by default.")

            theme = default_theme

    tree = ElementTree.parse(theme)
    theme = {child.attrib['name']: child.text for child in tree.getroot()}

    for k in theme:
        os.environ[str(k)] = theme[k]

    if light_secondary:
        theme['secondaryColor'], theme['secondaryLightColor'], theme['secondaryDarkColor'] = theme[
            'secondaryColor'], theme['secondaryDarkColor'], theme['secondaryLightColor']
        # 'secondaryColor': '#fafafa', 'secondaryLightColor': '#ffffff', 'secondaryDarkColor': '#c7c7c7'

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
        app.setStyle(style)
    stylesheet = build_stylesheet(theme, light_secondary, resources, extra)

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
def set_icons_theme(theme, resource=None, overwrite=False):
    """"""
    try:
        theme = get_theme(theme)
    except:
        pass

    if resource is None:
        resource = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), _resource)
    # else:
        # rsc =

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

        if not overwrite:
            exec(content, globals())
            return

    # if overwrite:
    with open(resource, 'w') as file:
        file.write(content)


# ----------------------------------------------------------------------
def list_themes():
    """"""
    themes = os.listdir(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'themes'))
    themes = filter(lambda a: a.endswith('xml'), themes)
    return list(themes)
