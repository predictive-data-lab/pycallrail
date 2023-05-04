import pytest
import pytest_mock

import os
import typing
from pycallrail.callrail import CallRail
from pycallrail.objects.accounts import Account
from pycallrail.objects.calls import Call
from pycallrail.objects.companies import Company
from pycallrail.objects.form_submissions import FormSubmission
from pycallrail.objects.textmessages import TextMessageConversation
import logging


@pytest.fixture(scope='module')
def callrail() -> typing.Generator[CallRail, None, None]:
    if os.getenv('CALLRAIL_API_KEY'):
        api_key: str = os.getenv('CALLRAIL_API_KEY')
    else:
        from . import cfg
        api_key = cfg.CALLRAIL_API_KEY

    yield CallRail(api_key)

@pytest.mark.integration
def test_list_accounts(callrail: CallRail) -> None:
    
    accounts = callrail.list_accounts()


    assert isinstance(accounts, list)
    assert isinstance(accounts[0], Account)
    
    # assert there are attributes in the response
    assert hasattr(accounts[0], 'id')
    assert hasattr(accounts[0], 'name')

@pytest.mark.integration
def test_list_calls(callrail: CallRail) -> None:

    accounts: typing.List[Account] = callrail.list_accounts()
    account: Account = accounts[0]

    calls: typing.List[Call] = account.list_calls()

    assert isinstance(calls, list)
    assert isinstance(calls[0], Call)

    # assert there are attributes in the response
    assert hasattr(calls[0], 'id')
    assert hasattr(calls[0], 'account_id')


@pytest.mark.integration
def test_list_companies(callrail: CallRail) -> None:

    accounts = callrail.list_accounts()
    account: Account = accounts[0]
    
    companies: typing.List[Account] = account.list_companies()

    assert isinstance(companies, list)
    assert isinstance(companies[0], Company)

    # assert there are attributes in the response
    assert hasattr(companies[0], 'id')
    assert hasattr(companies[0], 'name')

@pytest.mark.integration
def test_formsubmission(callrail: CallRail) -> None:

    accounts = callrail.list_accounts()
    account: Account = accounts[0]
    
    form_submissions: typing.List[FormSubmission] = account.list_form_submissions()
    
    assert isinstance(form_submissions, list)
    assert isinstance(form_submissions[0], FormSubmission)
    
    # assert there are attributes in the response
    assert hasattr(form_submissions[0], 'id')
    assert hasattr(form_submissions[0], 'account_id')
    assert hasattr(form_submissions[0], 'form_data')

@pytest.mark.integration
def test_list_text_messages(callrail: CallRail) -> None:

    accounts = callrail.list_accounts()
    account: Account = accounts[0]
    
    text_messages: typing.List[TextMessageConversation] = account.list_text_message_conversations()
    
    assert isinstance(text_messages, list)
    assert isinstance(text_messages[0], TextMessageConversation)
    
    # assert there are attributes in the response
    assert hasattr(text_messages[0], 'id')
    assert hasattr(text_messages[0], 'account_id')
    assert hasattr(text_messages[0], 'recent_messages')