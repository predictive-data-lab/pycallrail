from setuptools import setup
import os
this_directory = os.path.dirname(__file__)
readme_file = os.path.join(this_directory, 'readme.md')
readme = open(readme_file, encoding='utf-8').read()

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