"""
Setup script for creating macOS app bundle and DMG
"""

from setuptools import setup, find_packages
import os

APP = ['main.py']
DATA_FILES = []

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',  # Optional: add an icon file
    'plist': {
        'CFBundleDisplayName': 'SubRenamer',
        'CFBundleName': 'SubRenamer',
        'CFBundleIdentifier': 'com.subrenamer.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2024 SubRenamer',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.15.0',
    },
    'packages': ['tkinterdnd2'],
    'includes': ['tkinter', 'tkinterdnd2'],
    'excludes': ['tkinter.test'],
    'optimize': 2,
}

setup(
    name='SubRenamer',
    version='1.0.0',
    description='A macOS application for renaming subtitle files to match video files',
    author='SubRenamer Team',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    packages=find_packages(),
    install_requires=[
        'tkinterdnd2',
        'Pillow',
    ],
)