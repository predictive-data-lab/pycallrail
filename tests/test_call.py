import pytest
from unittest.mock import patch, MagicMock
from pytest_mock import MockerFixture
from requests_mock.mocker import Mocker
from pycallrail.callrail import CallRail
from pycallrail.api.accounts import Account
from pycallrail.api.call import Call, CallType
from requests import Response
from typing import Union, Generator
import requests_mock
import requests
import datetime as dt

# Tests that a Call object can be created with valid data. 
def test_create_call_object_with_valid_data(mocker: MockerFixture):
    # Arrange
    data = {
        "answered": True,
        'caller_id': '1234567890',
        'recording_enabled': True,
        'outbound_greeting_recording_url': 'http://example.com/greeting.mp3',
        'outbound_greeting_text': 'Hello',
        "business_phone_number": "123-456-7890",
        "customer_city": "New York",
        "customer_country": "USA",
        "customer_name": "John Doe",
        "customer_phone_number": "987-654-3210",
        "customer_state": "NY",
        "direction": "inbound",
        "duration": 120,
        "id": 1,
        'agent_id': '456',
        "recording": "https://example.com/recording.mp3",
        "recording_duration": "00:02:00",
        "recording_player": "https://example.com/recording_player.mp3",
        "start_time": dt.datetime.now(),
        "tracking_phone_number": "555-555-5555",
        "voicemail": False
    }
    parent_mock = mocker.Mock(spec=Account)
    call = Call(data, parent_mock)

    # Act
    result = call.__dict__()

    # Assert
    assert result == data

# Tests that a Call object can be updated with valid data. 
def test_update_call_object_with_valid_data(mocker: MockerFixture):
    # Arrange
    data = {
        'recording_enabled': True,
        'outbound_greeting_recording_url': 'http://example.com/greeting.mp3',
        'outbound_greeting_text': 'Hello',
        "agent_id": "456",
        "caller_id": "1234567890",
        "answered": True,
        "business_phone_number": "123-456-7890",
        "customer_city": "New York",
        "customer_country": "USA",
        "customer_name": "John Doe",
        "customer_phone_number": "987-654-3210",
        "customer_state": "NY",
        "direction": "inbound",
        "duration": 120,
        "id": 1,
        "recording": "https://example.com/recording.mp3",
        "recording_duration": "00:02:00",
        "recording_player": "https://example.com/recording_player.mp3",
        "start_time": dt.datetime.now().strftime,
        "tracking_phone_number": "555-555-5555",
        "voicemail": False
    }
    parent_parent_mock = mocker.Mock(spec=CallRail)
    acount = Account({}, parent_parent_mock)
    call = Call(data, acount)

    update_data = {
        "answered": False,
        "duration": 180
    }

    # Act
    # We have to patch the parent mock methods because the parent mock
    # is a child of the call object.
    with patch.object(parent_parent_mock, '_put') as mock_put:
        mock_put.return_value = data | update_data
        call.update(update_data)

    result = call.__dict__()

    # Assert
    expected_result = data.copy()
    expected_result['answered'] = False
    expected_result['duration'] = 180
    assert result == expected_result

# Tests that a Call object cannot be created with missing or invalid data. 
def test_create_call_object_with_missing_or_invalid_data(mocker: MockerFixture):
    # Arrange
    data = {
        "answered": True,
        "business_phone_number": "123-456-7890",
        "customer_city": "New York",
        "customer_country": "USA",
        "customer_name": "John Doe",
        "customer_phone_number": "987-654-3210",
        "customer_state": "NY",
        "direction": "inbound",
        "duration": 120,
        "id": 1,
        "recording": "https://example.com/recording.mp3",
        "recording_duration": "00:02:00",
        "recording_player": "https://example.com/recording_player.mp3",
        "start_time": dt.datetime.now(),
        "tracking_phone_number": "555-555-5555",
        "voicemail": False
    }
    parent_mock = mocker.Mock(spec=Account)

    # Act and Assert
    with pytest.raises(ValueError):
        Call(None, parent_mock)

    with pytest.raises(ValueError):
        Call({}, parent_mock)

    invalid_data = data.copy()
    invalid_data["start_time"] = "invalid_datetime"
    with pytest.raises(ValueError):
        Call(invalid_data, parent_mock)
    
# Tests that a Call object cannot be updated with missing or invalid data. 
def test_update_call_object_with_missing_or_invalid_data(mocker: MockerFixture):
    # Arrange
    data = {
        'recording_enabled': True,
        'outbound_greeting_recording_url': 'http://example.com/greeting.mp3',
        'outbound_greeting_text': 'Hello',
        "agent_id": "456",
        "caller_id": "1234567890",
        "answered": True,
        "business_phone_number": "123-456-7890",
        "customer_city": "New York",
        "customer_country": "USA",
        "customer_name": "John Doe",
        "customer_phone_number": "987-654-3210",
        "customer_state": "NY",
        "direction": "inbound",
        "duration": 120,
        "id": 1,
        "recording": "https://example.com/recording.mp3",
        "recording_duration": "00:02:00",
        "recording_player": "https://example.com/recording_player.mp3",
        "start_time": dt.datetime.now(),
        "tracking_phone_number": "555-555-5555",
        "voicemail": False
    }
    parent_mock = mocker.Mock(spec=CallRail)
    acount = Account({}, parent_mock)

    call = Call(data, acount)

    # Act and Assert
    with pytest.raises(ValueError):
        call.update(None)

    with pytest.raises(KeyError):
        call.update({})

    invalid_data = {"start_time": "invalid_datetime"}
    with pytest.raises(ValueError):
        with patch.object(parent_mock, '_put') as mock_put:
            mock_put.return_value = data | invalid_data
            call.update(invalid_data)

# Tests that a Call object can be refreshed with valid data. 
def test_refresh_call_object_with_valid_data(mocker: MockerFixture):
    # Arrange
    data = {
    'recording_enabled': True,
    'outbound_greeting_recording_url': 'http://example.com/greeting.mp3',
    'outbound_greeting_text': 'Hello',
    "agent_id": "456",
    "caller_id": "1234567890",
    "answered": True,
    "business_phone_number": "123-456-7890",
    "customer_city": "New York",
    "customer_country": "USA",
    "customer_name": "John Doe",
    "customer_phone_number": "987-654-3210",
    "customer_state": "NY",
    "direction": "inbound",
    "duration": 120,
    "id": 1,
    "recording": "https://example.com/recording.mp3",
    "recording_duration": "00:02:00",
    "recording_player": "https://example.com/recording_player.mp3",
    "start_time": dt.datetime.now(),
    "tracking_phone_number": "555-555-5555",
    "voicemail": False
}
    parent_mock = mocker.Mock(spec=Account)
    call = Call(data, parent_mock)

    new_data = data.copy()
    new_data["duration"] = 180
    parent_mock.get_call.return_value = new_data

    # Act
    # patch the parent get call method
    with patch.object(parent_mock, 'get_call') as get_call_mock:
        get_call_mock.return_value = new_data
        call._refresh()
        result = call.__dict__()

    # Assert
    assert result == new_data

# Tests that a Call object cannot be refreshed with missing or invalid data.  
def test_refresh_call_object_with_missing_or_invalid_data(mocker: MockerFixture):
    # Arrange
    data = {
    'recording_enabled': True,
    'outbound_greeting_recording_url': 'http://example.com/greeting.mp3',
    'outbound_greeting_text': 'Hello',
    "agent_id": "456",
    "caller_id": "1234567890",
    "answered": True,
    "business_phone_number": "123-456-7890",
    "customer_city": "New York",
    "customer_country": "USA",
    "customer_name": "John Doe",
    "customer_phone_number": "987-654-3210",
    "customer_state": "NY",
    "direction": "inbound",
    "duration": 120,
    "id": 1,
    "recording": "https://example.com/recording.mp3",
    "recording_duration": "00:02:00",
    "recording_player": "https://example.com/recording_player.mp3",
    "start_time": dt.datetime.now(),
    "tracking_phone_number": "555-555-5555",
    "voicemail": False
}
    account: MagicMock = mocker.MagicMock(spec=Account(data=None, parent=CallRail('<my api key>')))
    call = Call(data, parent=account)

    # Update data with missing or invalid values
    updated_data = data.copy()
    updated_data["customer_name"] = None
    updated_data["duration"] = -1

    # Mock API response with updated data
    mocker.patch.object(account.parent, "_put", return_value=updated_data)

    # Act
    call.update(updated_data)

    # Assert
    assert call.customer_name is None
    assert call.duration == -1
    account.parent._put.assert_called_once_with(
        endpoint='a',
        path=f'/{account.id}/calls/{call.id}.json',
        data=updated_data
    )