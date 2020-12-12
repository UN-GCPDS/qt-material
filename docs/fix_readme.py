import os


with open('../README.rst', 'r') as file:
    content = file.read()
content = content.replace('images/dark.gif', 'https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/images/dark.gif')
content = content.replace('images/light.gif', 'https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/images/light.gif')
end = content.find('Indices and tables')
with open('../README.rst', 'w') as file:
    file.write(content[:end])
