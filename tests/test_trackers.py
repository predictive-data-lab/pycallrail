import pytest
from unittest.mock import patch, MagicMock
from pytest_mock import MockerFixture
from requests_mock.mocker import Mocker
from pycallrail.callrail import CallRail
from pycallrail.api.accounts import Account
from pycallrail.api.trackers import Tracker
from pycallrail.api.companies import Company
from requests import Response
from typing import Union, Generator, Any, Dict
import requests_mock
import requests
import datetime as dt

# Tests that a Tracker object can be created with valid data. 
def test_creating_tracker_with_valid_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock(spec=Account)
    data: Dict[str, Any] = {
        'id': '123',
        'name': 'Test Tracker',
        'type': 'dynamic',
        'destination_number': '555-555-5555',
        'status': 'active',
        'tracking_number': '888-888-8888',
        'whisper_message': 'This is a test',
        'sms_enabled': True,
        'sms_supported': True,
        'company': {},
        'call_flow': {},
        'source': {},
        'created_at': '2022-01-01T00:00:00.000',
        'disabled_at': None,
        'campaign_name': None,
        'swap_targets': None
    }

    # Act
    tracker = Tracker(parent, data)

    # Assert
    assert tracker.id == '123'
    assert tracker.name == 'Test Tracker'
    assert tracker.type == 'dynamic'
    assert tracker.destination_number == '555-555-5555'
    assert tracker.status == 'active'
    assert tracker.tracking_number == '888-888-8888'
    assert tracker.whisper_message == 'This is a test'
    assert tracker.sms_enabled == True
    assert tracker.sms_supported == True
    assert isinstance(tracker.company, Company)
    assert isinstance(tracker.call_flow, dict)
    assert isinstance(tracker.source, dict)
    assert isinstance(tracker.created_at, dt.datetime)
    assert tracker.disabled_at == None
    assert tracker.campaign_name == None
    assert tracker.swap_targets == None

# Tests that data can be retrieved from a Tracker object. 
def test_retrieving_data_from_tracker(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock(spec=Account)
    data = {
        'id': '123',
        'name': 'Test Tracker',
        'type': 'dynamic',
        'destination_number': '555-555-5555',
        'status': 'active',
        'tracking_number': '888-888-8888',
        'whisper_message': 'This is a test',
        'sms_enabled': True,
        'sms_supported': True,
        'company': {},
        'call_flow': {},
        'source': {},
        'created_at': '2022-01-01T00:00:00.000',
        'disabled_at': None,
        'campaign_name': None,
        'swap_targets': None
    }
    tracker = Tracker(parent, data)

    # Act
    id = tracker.id
    name = tracker.name
    type = tracker.type
    destination_number = tracker.destination_number
    status = tracker.status
    tracking_number = tracker.tracking_number
    whisper_message = tracker.whisper_message
    sms_enabled = tracker.sms_enabled
    sms_supported = tracker.sms_supported
    company = tracker.company
    call_flow = tracker.call_flow
    source = tracker.source
    created_at = tracker.created_at
    disabled_at = tracker.disabled_at
    campaign_name = tracker.campaign_name
    swap_targets = tracker.swap_targets

    # Assert
    assert id == '123'
    assert name == 'Test Tracker'
    assert type == 'dynamic'
    assert destination_number == '555-555-5555'
    assert status == 'active'
    assert tracking_number == '888-888-8888'
    assert whisper_message == 'This is a test'
    assert sms_enabled == True
    assert sms_supported == True
    assert isinstance(company, Company)
    assert isinstance(call_flow, dict)
    assert isinstance(source, dict)
    assert isinstance(created_at, dt.datetime)
    assert disabled_at == None
    assert campaign_name == None
    assert swap_targets == None

# Tests that a Tracker object that is already disabled cannot be disabled again. 
def test_disabling_already_disabled_tracker(mocker: MockerFixture, caplog: pytest.LogCaptureFixture):
    # Arrange
    parent = mocker.Mock(spec=Account)
    data: Dict[str, Any] = {
        'id': '123',
        'name': 'Test Tracker',
        'type': 'dynamic',
        'destination_number': '555-555-5555',
        'status': 'disabled',
        'tracking_number': '888-888-8888',
        'whisper_message': 'This is a test',
        'sms_enabled': True,
        'sms_supported': True,
        'company': {},
        'call_flow': {},
        'source': {},
        'created_at': '2022-01-01T00:00:00.000',
        'disabled_at': '2022-01-02T00:00:00.000',
        'campaign_name': None,
        'swap_targets': None
    }
    tracker = Tracker(parent, data)

    # Act
    tracker.disable()

    # Assert that this was logged: logging.warning(f'Tracker {self.id} is already disabled')
    assert 'Tracker 123 is already disabled' in caplog.text

# Tests that a Tracker object that does not exist cannot be disabled. 
def test_disabling_nonexistent_tracker(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock(spec=CallRail)
    parent._delete.side_effect = Exception('Tracker not found')
    account = Account(data={}, parent=parent)
    data: Dict[str, Any] = {
        'id': '123',
        'name': 'Test Tracker',
        'type': 'dynamic',
        'destination_number': '555-555-5555',
        'status': 'active',
        'tracking_number': '888-888-8888',
        'whisper_message': 'This is a test',
        'sms_enabled': True,
        'sms_supported': True,
        'company': {},
        'call_flow': {},
        'source': {},
        'created_at': '2022-01-01T00:00:00.000',
        'disabled_at': None,
        'campaign_name': None,
        'swap_targets': None
    }
    tracker = Tracker(parent=account, data=data)

    # Act and Assert
    with pytest.raises(Exception):
        tracker.disable()

# Tests that a Tracker object cannot be created with missing or invalid data. 
def test_creating_tracker_with_missing_or_invalid_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    data: Dict[str, Any] = {
        'id': '123',
        'name': 'Test Tracker',
        'type': 'dynamic',
        'destination_number': '555-555-5555',
        'status': 'active',
        'tracking_number': '888-888-8888',
        'whisper_message': 'This is a test',
        'sms_enabled': True,
        'sms_supported': True,
        'company': {},
        'call_flow': {},
        'source': {},
        'created_at': '2022-01-01T00:00:00.000Z',
        'disabled_at': None,
        'campaign_name': None
    }

    # Act and Assert
    with pytest.raises(TypeError):
        tracker = Tracker(parent, data)

# Tests that a Tracker object's data can be updated. 
def test_updating_tracker_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock(spec=Account)
    data = {
        'id': '123',
        'name': 'Test Tracker',
        'type': 'dynamic',
        'destination_number': '555-555-5555',
        'status': 'active',
        'tracking_number': '888-888-8888',
        'whisper_message': 'This is a test',
        'sms_enabled': True,
        'sms_supported': True,
        'company': {},
        'call_flow': {},
        'source': {},
        'created_at': '2022-01-01T00:00:00.000',
        'disabled_at': None,
        'campaign_name': None,
        'swap_targets': None
    }
    tracker = Tracker(parent, data)

    # Act
    tracker.name = 'New Name'
    tracker.destination_number = '111-111-1111'

    # Assert
    assert tracker.name == 'New Name'
    assert tracker.destination_number == '111-111-1111'