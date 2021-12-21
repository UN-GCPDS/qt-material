import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
   README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='qt-material',
    version='2.8.15',
    packages=['qt_material',
              'qt_material.resources',
              'qt_material.resources.source'],

    author='Yeison Cardona',
    author_email='yencardonaal@unal.edu.co',
    maintainer='Yeison Cardona',
    maintainer_email='yencardonaal@unal.edu.co',

    download_url='https://github.com/UN-GCPDS/qt-material',

    install_requires=['Jinja2'],

    python_requires='>=3.7',

    include_package_data=True,
    license='BSD-2-Clause',
    description="Qt Stylesheet for PySide6, PySide2 and PyQt5.",
    long_description=README,
    long_description_content_type='text/markdown',

    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
    ],

    entry_points={
        "pyinstaller40": [
            "hook-dirs = qt_material:get_hook_dirs"
        ]
    },

)
