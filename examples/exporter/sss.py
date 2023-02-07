import PySide6

from qt_material import export_theme

export_theme(theme='dark_teal.xml',
             qss='dark_teal22.qss',
             rcc='resources22.rcc',
             output='theme',
             invert_secondary=False,
             )
