from setuptools import setup, find_packages
import os

setup(
    name='pycallrail',
    version='0.5.01',
    author = 'Khari Gardner',
    author_email = 'khgardner@proton.me',
    description= "Unofficial Python wrapper for the CallRail API",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/kharigardner/pycallrail',
    packages = find_packages(),
    install_requires = [
        'ujson',
        'aiohttp',
        'requests'
    ]
)