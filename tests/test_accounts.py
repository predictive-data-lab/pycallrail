import pytest
from unittest.mock import patch, MagicMock
from pytest_mock import MockerFixture
from requests_mock.mocker import Mocker
from pycallrail.callrail import CallRail
from pycallrail.api.accounts import Account
from pycallrail.api.call import Call, CallType
from pycallrail.api.tag import Tag
from pycallrail.api.companies import Company
from requests import Response
from typing import Union, Generator, Any
import requests_mock
import requests
import datetime as dt
import logging

# 
# Tests that create_call method successfully creates a call. 
def test_create_call_success(mocker: MockerFixture):
    # Arrange
    account_data: dict[str, Any] = {
        "id": "123",
        "name": "Test Account",
        "outbound_recording_enabled": True,
        "hipaa_account": False
    }
    parent_mock = mocker.Mock()
    parent_mock.request_delay = None
    call_data: dict[str, Any] = {
        "caller_id": "1234567890",
        "customer_phone_number": "0987654321",
        "business_phone_number": "5555555555",
        "recording_enabled": True,
        "outbound_greeting_recording_url": "http://example.com/greeting.mp3",
        "outbound_greeting_text": "Hello",
        "agent_id": "456",
        'outbound_greeting_text': 'Hello',
        'outbound_greeting_recording_url': 'http://example.com/greeting.mp3'
    }
    expected_call_json: dict[str, Any] = {
        "id": "456",
        "caller_id": "1234567890",
        "customer_phone_number": "0987654321",
        "business_phone_number": "5555555555",
        "recording_enabled": True,
        "outbound_greeting_recording_url": "http://example.com/greeting.mp3",
        "outbound_greeting_text": "Hello",
        "agent_id": "456"
    }
    parent_mock._post.return_value = expected_call_json
    account = Account(account_data, parent_mock)

    # Act
    call: Call = account.create_call(call_data)

    # Assert
    parent_mock._post.assert_called_once_with(endpoint='a', path='/123/calls.json', data=call_data)
    assert isinstance(call, Call)
    assert call.as_dict == expected_call_json

# Tests that get_call method successfully retrieves a call. 
def test_get_call_success(mocker: MockerFixture):
    # Arrange
    account_data = {
        "id": "123",
        "name": "Test Account",
        "outbound_recording_enabled": True,
        "hipaa_account": False
    }
    parent_mock = mocker.Mock()
    parent_mock.request_delay = None
    call_id = "456"
    expected_call_dict =  {
            "id": "456",
            "caller_id": "1234567890",
            "customer_phone_number": "0987654321",
            "business_phone_number": "5555555555",
            "recording_enabled": True,
            "outbound_greeting_recording_url": "http://example.com/greeting.mp3",
            "outbound_greeting_text": "Hello",
            "agent_id": "789"
        }
    parent_mock._get.return_value = expected_call_dict
    account = Account(account_data, parent_mock)

    # Act
    call = account.get_call(call_id)

    # Assert
    parent_mock._get.assert_called_once_with(endpoint='a', path='/123/calls/456.json', params={}, response_data_key='call')
    assert isinstance(call, Call)
    
    ExpectedCall = Call(expected_call_dict, Account({}, CallRail('123')))

    assert call.as_dict == ExpectedCall.as_dict

# Tests that get_tracker method returns None when tracker is None. 
def test_get_tracker_none(mocker: MockerFixture):
    # Arrange
    account_data = {
        "id": "123",
        "name": "Test Account",
        "outbound_recording_enabled": True,
        "hipaa_account": False
    }
    parent_mock = mocker.Mock()
    parent_mock.request_delay = None
    tracker_id = "456"
    parent_mock._get.return_value = None
    account = Account(account_data, parent_mock)

    # Act
    tracker = account.get_tracker(tracker_id)

    # Assert
    parent_mock._get.assert_called_once_with(endpoint='a', path='/123/trackers/456.json', params={})
    assert tracker is None

# Tests that create_tag method successfully creates a tag. 
def test_create_tag_success(mocker: MockerFixture):
    # Arrange
    account_data = {
        "id": "123",
        "name": "Test Account",
        "outbound_recording_enabled": True,
        "hipaa_account": False
    }
    parent_mock = mocker.Mock()
    parent_mock.request_delay = None
    tag_data: dict[str, Union[str, int]] = {
      "id": 993186,
      "name": "Conversion",
      "tag_level": "company",
      "color": "gray1",
      "background_color": "green2",
      "company_id": "COM37221d54e80c4216898d2f857fc69fa0",
      "status": "enabled",
      "created_at": "2017-07-24T11:13:47.366-04:00"
    }
    expected_tag_json: dict[str, Union[str, int]] = {
      "id": 993186,
      "name": "Conversion",
      "tag_level": "company",
      "color": "gray1",
      "background_color": "green2",
      "company_id": "COM37221d54e80c4216898d2f857fc69fa0",
      "status": "enabled",
      "created_at": "2017-07-24T11:13:47.366-04:00"
    }
    parent_mock._post.return_value = expected_tag_json
    account = Account(account_data, parent_mock)

    # Act
    tag: Tag = account.create_tag(tag_data)

    # Assert
    parent_mock._post.assert_called_once_with(endpoint='a', path='/123/tags.json', data=tag_data)
    assert isinstance(tag, Tag)
    assert tag.as_dict == expected_tag_json

# Tests that get_company method successfully retrieves a company. 
def test_get_company_success(mocker: MockerFixture):
    # Arrange
    account_data = {
        "id": "123",
        "name": "Test Account",
        "outbound_recording_enabled": True,
        "hipaa_account": False
    }
    parent_mock = mocker.Mock()
    parent_mock.request_delay = None
    company_id = "456"
    expected_company_dict = {
        "id": "456",
        "name": "Test Company"
    }
    parent_mock._get.return_value = expected_company_dict
    account = Account(account_data, parent_mock)

    # Act
    company = account.get_company(company_id)

    # Assert
    parent_mock._get.assert_called_once_with(endpoint='a', path='/123/companies/456.json')
    assert isinstance(company, Company)
    assert company.as_dict == expected_company_dict

# Tests that create_company method successfully creates a company. 
def test_create_company_success(mocker: MockerFixture):
    # Arrange
    account_data: dict[str, Any] = {
        "id": "123",
        "name": "Test Account",
        "outbound_recording_enabled": True,
        "hipaa_account": False
    }
    parent_mock = mocker.Mock()
    parent_mock.request_delay = None
    company_data: dict[str, str] = {
        "name": "Test Company"
    }
    expected_company_json: dict[str, str] = {
        "id": "456",
        "name": "Test Company"
    }
    parent_mock._post.return_value = expected_company_json
    account = Account(account_data, parent_mock)

    # Act
    company = account.create_company(company_data)

    # Assert
    parent_mock._post.assert_called_once_with(endpoint='a', path='/123/companies.json', data=company_data)
    assert isinstance(company, Company)
    assert company.as_dict == expected_company_json