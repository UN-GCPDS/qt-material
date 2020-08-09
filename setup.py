import os
from setuptools import setup, find_packages

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pyside-material',
    version='1.12',
    packages=['pyside_material', 'pyside_material.resources'],

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    # url='http://yeisoncardona.com/',
    download_url='https://bitbucket.org/gcpds/pyside-material/downloads/',

    install_requires=['pyside2',
                      # 'python-for-android', #install from git
                      ],

    include_package_data=True,
    license='BSD License',
    description="PySide2 stylesheet.",
    #    long_description = README,

    classifiers=[

    ],

)
