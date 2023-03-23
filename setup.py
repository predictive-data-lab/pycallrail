from setuptools import setup
import os

setup(
    name='pycallrail',
    version='0.5.0',
    author = 'Khari Gardner',
    author_email = 'khgardner@proton.me',
    description= "Unofficial Python wrapper for the CallRail API",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/kharigardner/pycallrail',
    packages = ['pycallrail'],
    install_requires = [
        'ujson',
        'aiohttp',
        'requests'
    ]
)