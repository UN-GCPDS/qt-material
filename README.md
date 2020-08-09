# PySide Material

This is another stylesheet for PySide, this time looks like Material Design.


There is some custom dark themes:

![Dark](https://github.com/UN-GCPDS/pyside-material/raw/master/docs/source/images/dark.gif)


And light:

![Light](https://github.com/UN-GCPDS/pyside-material/raw/master/docs/source/images/light.gif)


## Install

```bash
  pip install pyside-material
```

## Usage

```python
import sys
from PySide2 import QtWidgets
from pyside_material import apply_stylesheet

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

```
from pyside_material import list_themes

list_themes()
```

```
light_yellow.xml
light_teal.xml
dark_purple.xml
light_amber.xml
light_blue.xml
light_purple.xml
dark_pink.xml
light_cyan.xml
dark_blue.xml
dark_teal.xml
dark_lightgreen.xml
light_lightgreen.xml
light_pink.xml
dark_amber.xml
dark_cyan.xml
light_red.xml
dark_yellow.xml
dark_red.xml
```



# Custom colors

`Color Tool <https://material.io/resources/color//>`_ is the best way to
generate new themes, just choose colors and export as `Android XML`, the theme
file must look like:

```xml
<!--?xml version="1.0" encoding="UTF-8"?-->
<resources>
  <color name="primaryColor">#1de9b6</color>
  <color name="primaryLightColor">#6effe8</color>
  <color name="primaryDarkColor">#00b686</color>
  <color name="secondaryColor">#263238</color>
  <color name="secondaryLightColor">#4f5b62</color>
  <color name="secondaryDarkColor">#000a12</color>
  <color name="primaryTextColor">#000000</color>
  <color name="secondaryTextColor">#ffffff</color>
</resources>
```

Save it as `my_theme.xml` or similar and apply the style sheet from Python.

```python
apply_stylesheet(app, theme='dark_teal.xml')
```


# Light themes


Light will need to add `light_secondary` argument as `True`.

```python
apply_stylesheet(app, theme='dark_teal.xml', light_secondary=True)
```
