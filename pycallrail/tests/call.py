import unittest
import callrail as crl
from config import api_key
from api.call import Call

class TestCallAccountMethods(unittest.TestCase):
    """
    Test the various call related methods from the Account class.
    """
    def test_list_calls(self):
        cr = crl.CallRail(api_key=api_key)
        account = cr.get_account('ACCfc800e85eba74b62ae02ef58fd76b0db')
        callz = account.list_calls()
        # print a call id so I can use it in the next test
        print(callz[0].id)
        self.assertIsInstance(callz, list[Call])

    

    
