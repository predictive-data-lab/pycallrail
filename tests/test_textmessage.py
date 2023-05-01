import pytest
from unittest.mock import patch, MagicMock
from pytest_mock import MockerFixture
from requests_mock.mocker import Mocker
from pycallrail.callrail import CallRail
from pycallrail.api.accounts import Account
from pycallrail.api.textmessage import TextMessage, TextMessageThread
from requests import Response
from typing import Union, Generator, Any
import requests_mock
import requests
import datetime as dt

# Tests that the parent attribute is correctly set to a TextMessageThread instance. 
def test_init_sets_parent_attribute(mocker: MockerFixture) -> None:
    mock_parent = mocker.Mock(spec=TextMessageThread)
    data: dict[str, str] = {'direction': 'inbound', 'content': 'Hello', 'created_at': '2022-01-01T00:00:00'}
    text_message = TextMessage(mock_parent, data)
    assert text_message.parent == mock_parent

# Tests that the direction, content, and created_at attributes are correctly extracted from the input data. 
def test_init_extracts_attributes(mocker: MockerFixture):
    mock_parent = mocker.Mock(spec=TextMessageThread)
    data: dict[str, str] = {'direction': 'inbound', 'content': 'Hello', 'created_at': '2022-01-01T00:00:00'}
    text_message = TextMessage(mock_parent, data)
    assert text_message.direction == 'inbound'
    assert text_message.content == 'Hello'
    assert text_message.created_at == dt.datetime(2022, 1, 1, 0, 0)

# Tests that the constructor raises a TypeError if the parent argument is not a TextMessageThread instance. 
def test_init_raises_TypeError_if_parent_not_TextMessageThread(mocker: MockerFixture):
    class GarbageClass:
        pass
    wrong_class = GarbageClass()
    data: dict[str, str] = {'direction': 'inbound', 'content': 'Hello', 'created_at': '2022-01-01T00:00:00'}
    with pytest.raises(TypeError):
        TextMessage(wrong_class, data)

# Tests that the constructor raises a ValueError if the input data is missing any of the required keys. 
def test_init_raises_KeyError_if_missing_required_keys(mocker: MockerFixture):
    mock_parent = mocker.Mock(spec=TextMessageThread)
    data: dict[str, str] = {'direction': 'inbound', 'created_at': '2022-01-01T00:00:00'}
    with pytest.raises(KeyError):
        TextMessage(mock_parent, data)

# Tests that the TextMessage instance can be converted to a dictionary using the as_dict attribute. 
def test_as_dict_returns_dictionary_representation(mocker: MockerFixture):
    mock_parent = mocker.Mock(spec=TextMessageThread)
    data: dict[str, str] = {'direction': 'inbound', 'content': 'Hello', 'created_at': '2022-01-01T00:00:00'}
    text_message = TextMessage(mock_parent, data)
    assert text_message.as_dict == data

# Tests that the constructor raises a ValueError if the input data has an invalid value for any of the keys. 
def test_init_raises_ValueError_if_invalid_value_for_keys(mocker: MockerFixture):
    mock_parent = mocker.Mock(spec=TextMessageThread)
    data: dict[str, str] = {'direction': 'invalid', 'content': 'Hello', 'created_at': '2022-01-01T00:00:00'}
    with pytest.raises(ValueError):
        TextMessage(mock_parent, data)

# Tests creating a TextMessageThread object with valid data. 
def test_create_text_message_thread_valid_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    data = {
        'id': '123',
        'company_id': '456',
        'initial_tracker_id': '789',
        'current_tracker_id': '012',
        'customer_name': 'John Doe',
        'customer_phone_number': '123-456-7890',
        'initial_tracking_number': '111-111-1111',
        'current_tracking_number': '222-222-2222',
        'last_message_at': '2022-01-01T00:00:00.000',
        'state': 'active',
        'company_time_zone': 'America/New_York',
        'formatted_customer_phone_number': '(123) 456-7890',
        'formatted_initial_tracking_number': '(111) 111-1111',
        'formatted_current_tracking_number': '(222) 222-2222',
        'formatted_customer_name': 'John Doe',
        'recent_messages': [
            {
                'direction': 'inbound',
                'content': 'Hello',
                'created_at': '2022-01-01T00:00:00.000'
            },
            {
                'direction': 'outbound',
                'content': 'Hi there',
                'created_at': '2022-01-01T00:01:00.000'
            }
        ],
        'lead_status': 'new'
    }

    # Act
    text_message_thread = TextMessageThread(parent, data)

    # Assert
    assert text_message_thread.id == data['id']
    assert text_message_thread.company_id == data['company_id']
    assert text_message_thread.initial_tracker_id == data['initial_tracker_id']
    assert text_message_thread.current_tracker_id == data['current_tracker_id']
    assert text_message_thread.customer_name == data['customer_name']
    assert text_message_thread.customer_phone_number == data['customer_phone_number']
    assert text_message_thread.initial_tracking_number == data['initial_tracking_number']
    assert text_message_thread.current_tracking_number == data['current_tracking_number']
    assert text_message_thread.last_message_at == dt.datetime.fromisoformat(data['last_message_at'])
    assert text_message_thread.state == data['state']
    assert text_message_thread.company_time_zone == data['company_time_zone']
    assert text_message_thread.formatted_customer_phone_number == data['formatted_customer_phone_number']
    assert text_message_thread.formatted_initial_tracking_number == data['formatted_initial_tracking_number']
    assert text_message_thread.formatted_current_tracking_number == data['formatted_current_tracking_number']
    assert text_message_thread.formatted_customer_name == data['formatted_customer_name']
    assert isinstance(text_message_thread.recent_messages, list)
    assert all(isinstance(message, TextMessage) for message in text_message_thread.recent_messages)
    assert text_message_thread.lead_status == data['lead_status']

    # Tests sending a text message to a customer with valid data. 
def test_send_text_message_valid_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    parent.parent.request_delay = 0
    text_message_thread = TextMessageThread(parent, {'id': '123'})
    data: dict[str, str] = {
        'company_id': '456',
        'tracking_number': '111-111-1111',
        'customer_phone_number': '123-456-7890',
        'content': 'Hello'
    }
    expected_response: dict[str, str] = {'id': '456'}

    mocker.patch.object(parent.parent, '_post', return_value=expected_response)

    # Act
    result: TextMessageThread = text_message_thread.send_text_message(data)

    # Assert
    assert isinstance(result, TextMessageThread)
    assert result.id == text_message_thread.id

# Tests creating a TextMessageThread object with missing data. 
def test_create_text_message_thread_missing_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    data: dict[str, str] = {
        'id': '123',
        'company_id': '456',
        'initial_tracker_id': '789',
        'current_tracker_id': '012',
        'customer_name': 'John Doe',
        'customer_phone_number': '123-456-7890',
        'initial_tracking_number': '111-111-1111',
        'current_tracking_number': '222-222-2222',
        'last_message_at': '2022-01-01T00:00:00.000Z',
        'state': 'active',
        'company_time_zone': 'America/New_York',
        'formatted_customer_phone_number': '(123) 456-7890',
        'formatted_initial_tracking_number': '(111) 111-1111',
        'formatted_current_tracking_number': '(222) 222-2222',
        'formatted_customer_name': 'John Doe',
        # missing recent_messages
        'lead_status': 'new'
    }

    # Act & Assert
    with pytest.raises(KeyError):
        TextMessageThread(parent, data)

# Tests creating a TextMessageThread object with invalid data. 
def test_create_text_message_thread_invalid_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    data = {
        'id': '123',
        'company_id': '456',
        'initial_tracker_id': '789',
        'current_tracker_id': '012',
        'customer_name': 'John Doe',
        'customer_phone_number': '123-456-7890',
        'initial_tracking_number': '111-111-1111',
        'current_tracking_number': '222-222-2222',
        'last_message_at': '2022-01-01T00:00:00.000Z',
        'state': 'active',
        'company_time_zone': 'America/New_York',
        'formatted_customer_phone_number': '(123) 456-7890',
        'formatted_initial_tracking_number': '(111) 111-1111',
        'formatted_current_tracking_number': '(222) 222-2222',
        'formatted_customer_name': 'John Doe',
        'recent_messages': [
            {
                'direction': 'invalid',  # invalid direction
                'content': 'Hello',
                'created_at': '2022-01-01T00:00:00.000Z'
            },
            {
                'direction': 'outbound',
                'content': '',  # empty content
                'created_at': '2022-01-01T00:01:00.000Z'
            }
        ],
        'lead_status': 'new'
    }

    # Act & Assert
    with pytest.raises(ValueError):
        TextMessageThread(parent, data)

# Tests that TextMessageThread.recent_messages is a list of TextMessage objects. 
def test_recent_messages_type(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    data = {
        'id': '123',
        'company_id': '456',
        'initial_tracker_id': '789',
        'current_tracker_id': '012',
        'customer_name': 'John Doe',
        'customer_phone_number': '123-456-7890',
        'initial_tracking_number': '111-111-1111',
        'current_tracking_number': '222-222-2222',
        'last_message_at': '2022-01-01T00:00:00.000Z',
        'state': 'active',
        'company_time_zone': 'America/New_York',
        'formatted_customer_phone_number': '(123) 456-7890',
        'formatted_initial_tracking_number': '(111) 111-1111',
        'formatted_current_tracking_number': '(222) 222-2222',
        'formatted_customer_name': 'John Doe',
        'recent_messages': [
            {
                'direction': 'inbound',
                'content': 'Hello',
                'created_at': '2022-01-01T00:00:00.000Z'
            },
            {
                'direction': 'outbound',
                'content': 'Hi there',
                'created_at': '2022-01-01T00:01:00.000Z'
            }
        ],
        'lead_status': 'new'
    }

    # Act
    text_message_thread = TextMessageThread(parent, data)

    # Assert
    assert isinstance(text_message_thread.recent_messages, list)
    assert all(isinstance(message, TextMessage) for message in text_message_thread.recent_messages)

# Tests that TextMessageThread.send_text_message returns a TextMessageThread object. 
def test_send_text_message_returns_TextMessageThread(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    parent.parent.request_delay = 0
    text_message_thread = TextMessageThread(parent, {'id': '123'})
    data: dict[str, str] = {
        'company_id': '456',
        'tracking_number': '111-111-1111',
        'customer_phone_number': '123-456-7890',
        'content': 'Hello'
    }
    expected_response: dict[str, str] = {'id': '456'}

    mocker.patch.object(parent.parent, '_post', return_value=expected_response)

    # Act
    result: TextMessageThread = text_message_thread.send_text_message(data)

    # Assert
    assert isinstance(result, TextMessageThread)

# Tests handling exceptions raised by external dependencies. 
def test_handling_external_dependencies_exceptions(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    parent.parent.request_delay = 0
    text_message_thread = TextMessageThread(parent, {'id': '123'})
    data: dict[str, str] = {
        'company_id': '456',
        'tracking_number': '111-111-1111',
        'customer_phone_number': '123-456-7890',
        'content': 'Hello'
    }

    mocker.patch.object(parent.parent, '_post', side_effect=Exception('Something went wrong'))

    # Act & Assert
    with pytest.raises(Exception):
        text_message_thread.send_text_message(data)

# Tests handling network errors. 
def test_handling_network_errors(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    parent.parent.request_delay = 0
    text_message_thread = TextMessageThread(parent, {'id': '123'})
    data: dict[str, str] = {
        'company_id': '456',
        'tracking_number': '111-111-1111',
        'customer_phone_number': '123-456-7890',
        'content': 'Hello'
    }

    mocker.patch.object(parent.parent, '_post', side_effect=requests.exceptions.RequestException)

    # Act & Assert
    with pytest.raises(requests.exceptions.RequestException):
        text_message_thread.send_text_message(data)

# Tests sending a text message to a customer with missing data. 
def test_send_text_message_missing_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    parent.parent.request_delay = 0
    text_message_thread = TextMessageThread(parent, {'id': '123'})
    data = {
        # missing company_id
        'tracking_number': '111-111-1111',
        'customer_phone_number': '123-456-7890',
        'content': 'Hello'
    }

    # Act & Assert
    with pytest.raises(ValueError):
        text_message_thread.send_text_message(data)

# Tests sending a text message to a customer with invalid data. 
def test_send_text_message_invalid_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock(spec=Account)
    parent.parent.request_delay = 0
    text_message_thread = TextMessageThread(parent, {
      "id": "KZaGR",
      "company_id": "COM8154748ae6bd4e278a7cddd38a662f4f",
      "initial_tracker_id": "TRK8154748ae6bd4e278a7cddd38a662f4f",
      "current_tracker_id": "TRK8154748ae6bd4e278a7cddd38a662f5f",
      "customer_name": "MANN KEVIN",
      "customer_phone_number": "+14042223333",
      "initial_tracking_number": "+14045556677",
      "current_tracking_number": "+17703334455",
      "last_message_at": "2016-07-28T19:26:43.578Z",
      "state": "active",
      "company_time_zone": "America/New_York",
      "formatted_customer_phone_number": "404-222-3333",
      "formatted_initial_tracking_number": "404-555-6677",
      "formatted_current_tracking_number": "770-333-4455",
      "formatted_customer_name": "Mann Kevin",
      "recent_messages": [
        {
          "direction": "outgoing",
          "content": "Awww! But I was going into Tosche Station to pick up some power converters!",
          "created_at": "2016-07-28T19:28:21.578Z"
        },
        {
          "direction": "incoming",
          "content": "Take these two over to the garage, will you?  I want them cleaned up before dinner.",
          "created_at": "2016-07-28T19:26:43.578Z"
        }
      ]
    })
    data: dict[str, str] = {
        'company_id': '456',
        'tracking_number': '111-111-1111',
        'customer_phone_number': '123-456-7890',
        'content': 'Hello',
        'invalid_key': 'invalid_value'  # invalid key
    }

    # Act & Assert
    with pytest.raises(ValueError):
        text_message_thread.send_text_message(data)

# Tests archiving a text message thread. 
def test_archive_text_message_thread(self, mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    parent.parent.request_delay = 0
    text_message_thread = TextMessageThread(parent, {'id': '123'})

    mocker.patch.object(parent.parent, '_put')

    # Act
    text_message_thread.archive()

    # Assert
    parent.parent._put.assert_called_once_with(
        endpoint='a',
        path=f'/{parent.id}/text-messages/{text_message_thread.id}/archive.json',
        data={'state': 'archived'}
    )