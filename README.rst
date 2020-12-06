.. Qt Material documentation master file, created by
   sphinx-quickstart on Wed Aug  7 20:30:20 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Qt Material
===========

This is another stylesheet for **PySide2** and **PyQt5**, this time looks like Material
Design (close enough).

|GitHub top language| |PyPI - License| |PyPI| |PyPI - Status| |PyPI -
Python Version| |GitHub last commit| |CodeFactor Grade| |Documentation
Status|


There is some custom dark themes:

.. image:: https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/images/dark.gif


And light:

.. image:: https://github.com/UN-GCPDS/qt-material/raw/master/docs/source/images/light.gif


Install
-------

.. code:: bash

  pip install qt-material


Usage
-----

.. code:: python

  import sys
  from PySide2 import QtWidgets
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


Themes
------

.. code:: python

    from qt_material import list_themes

    list_themes()


.. code:: bash

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




Custom colors
-------------

`Color Tool <https://material.io/resources/color//>`_ is the best way to
generate new themes, just choose colors and export as `Android XML`, the theme
file must look like:

.. code:: xml

  <!--?xml version="1.0" encoding="UTF-8"?-->
  <resources>
    <color name="primaryColor">#00e5ff</color>
    <color name="primaryLightColor">#6effff</color>
    <color name="primaryDarkColor">#00b2cc</color>
    <color name="secondaryColor">#f5f5f5</color>
    <color name="secondaryLightColor">#ffffff</color>
    <color name="secondaryDarkColor">#e6e6e6</color>
    <color name="primaryTextColor">#000000</color>
    <color name="secondaryTextColor">#000000</color>
  </resources>


Save it as `my_theme.xml` or similar and apply the style sheet from Python.

.. code:: python

  apply_stylesheet(app, theme='dark_teal.xml')



Light themes
------------

Light will need to add `light_secondary` argument as `True`.

.. code:: python

  apply_stylesheet(app, theme='dark_teal.xml', light_secondary=True)




.. |GitHub top language| image:: https://img.shields.io/github/languages/top/un-gcpds/qt-material
.. |PyPI - License| image:: https://img.shields.io/pypi/l/qt-material
.. |PyPI| image:: https://img.shields.io/pypi/v/qt-material
.. |PyPI - Status| image:: https://img.shields.io/pypi/status/qt-material
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/qt-material
.. |GitHub last commit| image:: https://img.shields.io/github/last-commit/un-gcpds/qt-material
.. |CodeFactor Grade| image:: https://img.shields.io/codefactor/grade/github/UN-GCPDS/qt-material
.. |Documentation Status| image:: https://readthedocs.org/projects/qt-material/badge/?version=latest
   :target: https://qt-material.readthedocs.io/en/latest/?badge=latest





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
