Qt-Material
===========
This is another stylesheet for **PySide6**, **PySide2** and **PyQt5**, which looks like Material Design (close enough).

![GitHub top language](https://img.shields.io/github/languages/top/un-gcpds/qt-material)
![PyPI - License](https://img.shields.io/pypi/l/qt-material)
![PyPI](https://img.shields.io/pypi/v/qt-material)
![PyPI - Status](https://img.shields.io/pypi/status/qt-material)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qt-material)
![GitHub last commit](https://img.shields.io/github/last-commit/un-gcpds/qt-material)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/UN-GCPDS/qt-material)
[![Documentation Status](https://readthedocs.org/projects/qt-material/badge/?version=latest)](https://qt-material.readthedocs.io/en/latest/?badge=latest)

There is some custom dark themes:
![dark](https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/dark.gif)
And light:
![light](https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/light.gif)

## Navigation

  * [Install](#install)
  * [Usage](#usage)
  * [Themes](#themes)
  * [Custom colors](#custom-colors)
  * [Usage](#usage)
  * [Light themes](#light-themes)
  * [Extra colors and custom fonts](#extra-colors-and-custom-fonts)
  * [Run examples](#run-examples)
  * [New themes](#new-themes)
  * [Change theme in runtime](#change-theme-in-runtime)

## Install


```python
pip install qt-material
```

## Usage


```python
import sys
from PySide6 import QtWidgets
# from PySide2 import QtWidgets
# from PyQt5 import QtWidgets
from qt_material import apply_stylesheet

# create the application and the main window
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

# setup stylesheet
apply_stylesheet(app, theme='dark_teal.xml')

# run
window.show()
app.exec_()
```

## Themes


```python
from qt_material import list_themes

list_themes()
```

    WARNING:root:qt_material must be imported after PySide or PyQt!





    ['dark_amber.xml',
     'dark_blue.xml',
     'dark_cyan.xml',
     'dark_lightgreen.xml',
     'dark_pink.xml',
     'dark_purple.xml',
     'dark_red.xml',
     'dark_teal.xml',
     'dark_yellow.xml',
     'light_amber.xml',
     'light_blue.xml',
     'light_cyan.xml',
     'light_cyan_500.xml',
     'light_lightgreen.xml',
     'light_pink.xml',
     'light_purple.xml',
     'light_red.xml',
     'light_teal.xml',
     'light_yellow.xml']



## Custom colors

[Color Tool](https://material.io/resources/color/) is the best way to generate new themes, just choose colors and export as `Android XML`, the theme file must look like:


```python
<!--?xml version="1.0" encoding="UTF-8"?-->
<resources>
<color name="primaryColor">#00e5ff</color>
<color name="primaryLightColor">#6effff</color>
<color name="secondaryColor">#f5f5f5</color>
<color name="secondaryLightColor">#ffffff</color>
<color name="secondaryDarkColor">#e6e6e6</color>
<color name="primaryTextColor">#000000</color>
<color name="secondaryTextColor">#000000</color>
</resources>
```

Save it as `my_theme.xml` or similar and apply the style sheet from Python.


```python
apply_stylesheet(app, theme='dark_teal.xml')
```

## Light themes
Light themes will need to add `invert_secondary` argument as `True`.


```python
apply_stylesheet(app, theme='light_red.xml', invert_secondary=True)
```

## Extra colors and custom fonts

There is an `extra` argument for accent colors and custom fonts. 


```python
extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font-family': 'Roboto',
}

apply_stylesheet(app, 'light_cyan.xml', invert_secondary=True, extra=extra)
```

The accent colors are applied to `QPushButton` with the corresponding `class`  property:


```python
pushButton_danger.setProperty('class', 'danger')
pushButton_warning.setProperty('class', 'warning')
pushButton_success.setProperty('class', 'success')
```

![extra](https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/extra.png)

## Run examples
A window with almost all widgets (see the previous screenshots) are available to test all themes and **create new ones**.


```python
git clone https://github.com/UN-GCPDS/qt-material.git
cd qt-material
python setup.py install
cd test
python main.py --PySide6
```

![theme](https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/theme.gif)

## New themes

Do you have a custom theme? it looks good? create a [pull request](https://github.com/UN-GCPDS/qt-material/pulls) in [themes folder](https://github.com/UN-GCPDS/qt-material/tree/master/qt_material/themes>)  and share it with all users.


## Change theme in runtime

There is a `qt_material.QtStyleTools` class that must be inherited along to `QMainWindow` for change themes in runtime using the `apply_stylesheet()` method.


```python
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    
    def __init__(self):
        super().__init__()
        self.main = QUiLoader().load('main_window.ui', self)
        
        self.apply_stylesheet(self.main, 'dark_teal.xml')
        # self.apply_stylesheet(self.main, 'light_red.xml')
        # self.apply_stylesheet(self.main, 'light_blue.xml')
```

![run](https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/runtime.gif)

### Integrate stylesheets in a menu

A custom _stylesheets menu_ can be added to a project for switching across all default available themes.


```python
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    
    def __init__(self):
        super().__init__()
        self.main = QUiLoader().load('main_window.ui', self)
        
        self.add_menu_theme(self.main, self.main.menuStyles)
```

![menu](https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/runtime_menu.gif)

## Create new themes

A simple interface is available to modify a theme in runtime, this feature can be used to create a new theme, the theme file is created in the main directory as `my_theme.xml`


```python
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    
    def __init__(self):
        super().__init__()
        self.main = QUiLoader().load('main_window.ui', self)
        
        self.show_dock_theme(self.main)
```

![dock](https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/runtime_dock.gif)

A full set of examples are available in the [exmaples directory](https://github.com/UN-GCPDS/qt-material/blob/master/examples/runtime/)
