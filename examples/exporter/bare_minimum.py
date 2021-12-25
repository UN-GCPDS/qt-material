import sys

from PySide6 import QtWidgets
from PySide6.QtCore import QDir
from __feature__ import snake_case, true_property

# Create application
app = QtWidgets.QApplication(sys.argv)

# Load styles
with open('dark_teal.qss', 'r') as file:
    app.style_sheet = file.read()

# Load icons
QDir.add_search_path('icon', 'theme')

# App
window = QtWidgets.QMainWindow()
checkbox = QtWidgets.QCheckBox(window)
checkbox.text = 'CheckBox'
window.show()
app.exec()
