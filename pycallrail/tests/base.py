# Base test to see if the API parent class is working

import unittest
import callrail as crl
from config import api_key
from api.accounts import Account

class TestBase(unittest.TestCase):
    def test_base(self):
        cr = crl.CallRail(api_key=api_key)
        self.assertIsInstance(cr, crl.CallRail)

# test to see if the api key is not set there is an error
class TestBaseError(unittest.TestCase):
    def test_base_error(self):
        with self.assertRaises(Exception):
            cr = crl.CallRail()

# test to see if we list accounts when using the list_accounts method
class TestListAccounts(unittest.TestCase):
    def test_list_accounts(self):
        cr = crl.CallRail(api_key=api_key)
        # i know this should be a single account since the api key is scoped to a single account
        self.assertIsInstance(cr.list_accounts(), Account)

# test to see if we can get an account by id
class TestGetAccountById(unittest.TestCase):
    def test_get_account_by_id(self):
        cr = crl.CallRail(api_key=api_key)
        self.assertIsInstance(cr.get_account('ACCfc800e85eba74b62ae02ef58fd76b0db'), Account)
