from qt_material import export_theme

extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'monoespace',
    'font_size': '13px',
    'line_height': '13px',

    # Density Scale
    'density_scale': '0',

    # environ
    'pyside6': True,
    'linux': True,

}


export_theme(theme='dark_teal.xml', qss='dark_teal.qss', rcc='resources.rcc',
             output='theme', prefix='icon:/', invert_secondary=False, extra=extra)



