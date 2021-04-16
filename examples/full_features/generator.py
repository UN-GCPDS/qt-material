import os

from qt_material import list_themes

themes = list_themes()
themes = [t.replace('.xml', '') for t in themes]

for theme in themes:
    os.system(f'python main.py --pyside6 {theme}')

os.chdir('screenshots')

commands = (
    'convert -delay 100 light_* light.gif',
    'convert -delay 100 dark_* dark.gif',
    # 'rm ../../../docs/source/images/light.gif',
    # 'rm ../../../docs/source/images/dark.gif',
    # 'cp light.gif ../../../docs/source/images/light.gif',
    # 'cp dark.gif ../../../docs/source/images/dark.gif',
    # 'cp theme.png ../../../docs/source/images/theme.png',
)

for command in commands:
    os.system(command)
