import os


with open('../README.md', 'r') as file:
    content = file.read()
content = content.replace('_images/dark.gif', 'https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/dark.gif')
content = content.replace('_images/light.gif', 'https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/light.gif')
content = content.replace('_images/theme.gif', 'https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/theme.gif')
with open('../README.md', 'w') as file:
    file.write(content)
