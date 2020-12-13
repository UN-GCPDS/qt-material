Qt Material
===========

This is another stylesheet for **PySide6**, **PySide2** and **PyQt5**,
which looks like Material Design (close enough).

|GitHub top language| |PyPI - License| |PyPI| |PyPI - Status| |PyPI -
Python Version| |GitHub last commit| |CodeFactor Grade| |Documentation
Status|

.. |GitHub top language| image:: https://img.shields.io/github/languages/top/un-gcpds/qt-material
.. |PyPI - License| image:: https://img.shields.io/pypi/l/qt-material
.. |PyPI| image:: https://img.shields.io/pypi/v/qt-material
.. |PyPI - Status| image:: https://img.shields.io/pypi/status/qt-material
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/qt-material
.. |GitHub last commit| image:: https://img.shields.io/github/last-commit/un-gcpds/qt-material
.. |CodeFactor Grade| image:: https://img.shields.io/codefactor/grade/github/UN-GCPDS/qt-material
.. |Documentation Status| image:: https://readthedocs.org/projects/qt-material/badge/?version=latest
   :target: https://qt-material.readthedocs.io/en/latest/?badge=latest

There is some custom dark themes: |dark| And light: |light|

.. |dark| image:: _images/dark.gif
.. |light| image:: _images/light.gif

Install
-------

.. code:: ipython3

    pip install qt-material

Usage
-----

.. code:: ipython3

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

Themes
------

.. code:: ipython3

    from qt_material import list_themes
    
    list_themes()


.. parsed-literal::

    WARNING:root:qt_material must be imported after PySide or PyQt!




.. parsed-literal::

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



Custom colors
-------------

`Color Tool <https://material.io/resources/color/>`__ is the best way to
generate new themes, just choose colors and export as ``Android XML``,
the theme file must look like:

.. code:: ipython3

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

Save it as ``my_theme.xml`` or similar and apply the style sheet from
Python.

.. code:: ipython3

    apply_stylesheet(app, theme='dark_teal.xml')

Light themes
------------

Light themes will need to add ``invert_secondary`` argument as ``True``.

.. code:: ipython3

    apply_stylesheet(app, theme='light_red.xml', invert_secondary=True)

Run example
-----------

A window with almost all widgets (see the previous screenshots) are
available to test all themes and **create new ones**.

.. code:: ipython3

    git clone https://github.com/UN-GCPDS/qt-material.git
    cd qt-material
    python setup.py install
    cd test
    python main.py --PySide6

| |theme|

.. |theme| image:: _images/theme.gif

New themes
----------

Do you have a custom theme? it looks good? create a `pull
request <https://github.com/UN-GCPDS/qt-material/pulls>`__ in `themes
folder <https://github.com/UN-GCPDS/qt-material/tree/master/qt_material/themes%3E>`__
and share it with all users.
