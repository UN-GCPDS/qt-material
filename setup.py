import os
from setuptools import setup, find_packages

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pyside-material',
    version='1.17',
    packages=['pyside_material', 'pyside_material.resources'],

    author='Yeison Cardona',
    author_email='yencardonaal@unal.edu.co',
    maintainer='Yeison Cardona',
    maintainer_email='yencardonaal@unal.edu.co',

    download_url='https://github.com/UN-GCPDS/pyside-material',

    install_requires=['pyside2',
                      ],

    python_requires='>=3.6',

    include_package_data=True,
    license='BSD-2-Clause',
    description="PySide2 stylesheet.",
    #    long_description = README,

    classifiers=[

    ],

)
