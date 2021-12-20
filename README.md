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
  * [Environ variables](#environ-variables)
  * [Alternative QPushButtons and custom fonts](#alternative-qpushbuttons-and-custom-fonts)
  * [Custom stylesheets](#custom-stylesheets)
  * [Run examples](#run-examples)
  * [New themes](#new-themes)
  * [Change theme in runtime](#change-theme-in-runtime)
  * [Density scale](#density-scale)

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

## Environ variables

There is a environ variables related to the current theme used, these variables are for **consult purpose only**.


| Environ variable               | Description                              | Example        |
|--------------------------------|------------------------------------------|----------------|
| QTMATERIAL_PRIMARYCOLOR        | Primary color                            | #2979ff        |
| QTMATERIAL_PRIMARYLIGHTCOLOR   | A bright version of the primary color    | #75a7ff        |
| QTMATERIAL_SECONDARYCOLOR      | Secondary color                          | #f5f5f5        |
| QTMATERIAL_SECONDARYLIGHTCOLOR | A bright version of the secondary color  | #ffffff        |
| QTMATERIAL_SECONDARYDARKCOLOR  | A dark version of the primary color      | #e6e6e6        |
| QTMATERIAL_PRIMARYTEXTCOLOR    | Color for text over primary background   | #000000        |
| QTMATERIAL_SECONDARYTEXTCOLOR  | Color for text over secondary background | #000000        |
| QTMATERIAL_THEME               | Name of theme used                       | light_blue.xml |

## Alternative QPushButtons and custom fonts

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

## Custom stylesheets

Custom changes can be performed by overwriting the stylesheets, for example:


```python
QPushButton {{
  color: {QTMATERIAL_SECONDARYCOLOR};
  text-transform: none;
  background-color: {QTMATERIAL_PRIMARYCOLOR};
}}

.big_button {{
  height: 64px;
}}
```

Then, the current stylesheet can be extended just with:


```python
apply_stylesheet(app, theme='light_blue.xml')

stylesheet = app.styleSheet()
with open('custom.css') as file:
    app.setStyleSheet(stylesheet + file.read().format(**os.environ))
```

And the class style can be applied with the `setProperty` method:


```python
self.main.pushButton.setProperty('class', 'big_button')
```

![extra](https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/custom.png)

## Run examples
A window with almost all widgets (see the previous screenshots) are available to test all themes and **create new ones**.


```
git clone https://github.com/UN-GCPDS/qt-material.git
cd qt-material
python setup.py install
cd examples/full_features
python main.py --pyside6
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

## Density scale

The ``extra`` arguments also include an option to set the **density scale**, by default is ```0```.


```python
extra = {
    
    # Density Scale
    'density_scale': '-2',
}

apply_stylesheet(app, 'default', invert_secondary=False, extra=extra)
```

![dock](https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/notebooks/_images/density/density.gif)
