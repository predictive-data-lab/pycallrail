pycallrail
==========

.. image:: https://img.shields.io/pypi/v/pycallrail.svg
   :target: https://pypi.python.org/pypi/pycallrail
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/pycallrail.svg
   :target: https://pypi.python.org/pypi/pycallrail.py
   :alt: PyPI supported Python versions
.. image:: https://github.com/predictive-data-lab/pycallrail/actions/workflows/test.yml/badge.svg
   :target: https://github.com/predictive-data-lab/pycallrail/commits/main
   :alt: GitHub Actions build status
.. image:: https://codecov.io/gh/predictive-data-lab/pycallrail/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/predictive-data-lab/pycallrail
   :alt: Codecov coverage report
.. image:: https://readthedocs.org/projects/pycallrail/badge/?version=latest
   :target: https://pycallrail.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Python wrapper for the CallRail API.

Description
-----------

This library provides a Python intefrace for interacting with the Callrail API.
It allows for CRUD operations on objects and resources within your CallRail account and to integrate
with your own applications.

Installation
------------
Install from PyPI using pip, a package manager for Python.

.. code:: sh

   # Linux/macOS
   python3 -m pip install pycallrail

   # Windows
   py -3 -m pip install pycallrail

Requirements & Dependencies
---------------------------
- Python 3.6+
- requests
- ujson
- python-dateutil
- typeguard

Usage
-----

.. code:: py

   import pycallrail.callrail as clrl

   # init the api client

   api = clrl.CallRail('your_api_key')

   # list accounts associated with your api key
   accounts = api.list_accounts(# optional kwargs, more info on supported kwargs at endpoint docs)

   # list calls associated with your account
   calls = accounts[0].list_calls(# optional kwargs, more info on supported kwargs at endpoint docs)

   print(calls[0].id) # prints the id of the first call in the list

   # >>> 123456789

Links & Contact
---------------

- `Documentation <https://pycallrail.readthedocs.io/en/latest/>`_
- `Questions <mailto:engineering@predictivedatalab.com>`_