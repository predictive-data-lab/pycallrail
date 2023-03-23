# Base test to see if the API parent class is working

import unittest as unittest
import callrail as crl
import os
from api.accounts import Account
from unittest import mock

api_key = os.environ.get("API_KEY")

class TestBase(unittest.TestCase):
    def setUp(self):
        self.cr = crl.CallRail(api_key=api_key)
    
    def tearDown(self):
        self.cr = None

    def test_init(self):
        self.assertIsInstance(self.cr, crl.CallRail)

    def test_init_with_no_api_key(self):
        with self.assertRaises(Exception):
            crl.CallRail()

    @mock.patch('callrail.CallRail.list_accounts')
    def test_list_accounts(self, mock_list_accounts):
        mock_list_accounts.return_value = Account(data=
        {
            "id": "ACCfc800e85eba74b62ae02ef58fd76b0db",
            "name": "Fresh Coat Painters",
            "numeric_id": 673960154,
            "outbound_recording_enabled": False,
            "hipaa_account": False,
            "agency_in_trial": False,
            "has_zuora_account": True,
            "created_at": "2021-03-25 13:34:18 -0400",
            "brand_status": None
        },
        parent=self.cr)

        accounts = self.cr.list_accounts()
        mock_list_accounts.assert_called_once()

        self.assertIsInstance(accounts, Account)
        self.assertEqual(accounts.id, "ACCfc800e85eba74b62ae02ef58fd76b0db")

    @mock.patch('callrail.CallRail.get_account')
    def test_get_account_by_id(self, mock_get_account):
        mock_get_account.return_value = Account(data=
        {
            "id": "ACCfc800e85eba74b62ae02ef58fd76b0db",
            "name": "Fresh Coat Painters",
            "numeric_id": 673960154,
            "outbound_recording_enabled": False,
            "hipaa_account": False,
            "agency_in_trial": False,
            "has_zuora_account": True,
            "created_at": "2021-03-25 13:34:18 -0400",
            "brand_status": None
        },
        parent=self.cr)

        account = self.cr.get_account("ACCfc800e85eba74b62ae02ef58fd76b0db")
        mock_get_account.assert_called_once()

        self.assertIsInstance(account, Account)
        self.assertEqual(account.id, "ACCfc800e85eba74b62ae02ef58fd76b0db")
