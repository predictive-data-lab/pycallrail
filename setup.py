from setuptools import setup, find_packages
import os
import re

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('pycallrail/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

if version.endswith(('a', 'b', 'rc')):
    try:
        import subprocess

        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode().strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception:
        pass

readme = ''
with open('README.rst') as f:
    readme = f.read()

extras_require = {
    'docs': [
        'sphinx==4.4.0',
        'sphinxcontrib_trio',
        'sphinxcontrib-websupport',
        'typing-extensions>=4.3.0'
    ],
    'test': [
        'coverage[toml]',
        'pytest',
        'pytest-mock',
        'pytest-cov',
        'typing-extensions>=4.3.0',
        'requests_mock',
        'typeguard',
        'python-dateutil'
    ]
}

packages = [
    'pycallrail'
    '.objects'
]

setup(
    name='pycallrail',
    author='Engineering @ Predictive Data Lab',
    url='https://github.com/predictive-data-lab/pycallrail',
    project_urls={
        'Documentation': 'https://pycallrail.readthedocs.io/en/latest/',
        'Issue Tracker': 'https://github.com/predictive-data-lab/pycallrail/issues'
    },
    version=version,
    packages=packages,
    license='MIT',
    description='An unofficial Python wrapper for the CallRail API',
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires='>=3.8.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Communications'
    ]
)