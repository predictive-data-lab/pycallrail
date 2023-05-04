import pytest
import pytest_mock
import requests_mock
import requests

from pycallrail.callrail import CallRail
from pycallrail.objects.textmessages import TextMessage, TextMessageConversation
import typing
import logging
import datetime as dt
import typeguard
import dataclasses

# Tests that a TextMessage object can be created with valid parameters. 
def test_creating_valid_text_message() -> None:
    direction = "outgoing"
    content = "Hello, this is a test message."
    created_at: dt.datetime = dt.datetime.now()
    text_message = TextMessage(direction=direction, content=content, created_at=created_at)
    assert text_message.direction == direction
    assert text_message.content == content
    assert text_message.created_at == created_at

# Tests that a TextMessage object cannot be created with empty string parameters. 
def test_empty_string_parameters() -> None:
    with pytest.raises(ValueError):
        direction = ""
        content = "Hello, this is a test message."
        created_at: dt.datetime = dt.datetime.now()
        TextMessage(direction=direction, content=content, created_at=created_at)

# Tests that a TextMessage object cannot be created with an invalid datetime format. 
def test_invalid_datetime_format() -> None:
    with pytest.raises(ValueError):
        direction = "outgpomg"
        content = "Hello, this is a test message."
        created_at = "2022-13-01 12:00:00"
        TextMessage(direction=direction, content=content, created_at=created_at)

# Tests that accessing the id attribute of a TextMessage object that has not been set returns None. 
def test_accessing_unset_id_attribute() -> None:
    text_message = TextMessage(
        direction="outgoing", 
        content="Hello, this is a test message.", 
        created_at=dt.datetime.now())
    assert text_message.id is None

# Tests archiving a TextMessageConversation. 
def test_archive_conversation(mocker: pytest_mock.MockerFixture) -> None:
    # Happy path test for archiving a TextMessageConversation
    api_client = CallRail('test_key')
    account_id = 'test_account'
    conversation_id = 'test_conversation'
    conversation_data: typing.Dict[str, str] = {
        'id': conversation_id,
        'state': 'active'
    }
    conversation = TextMessageConversation(api_client, account_id, **conversation_data)

    # Mock the _put method of the api_client to simulate a successful archive request
    mocker.patch.object(api_client, '_put', return_value=None)

    conversation.archive()

    assert conversation.state == 'archived'

# Tests creating a TextMessageConversation object with valid arguments. 
def test_create_text_message_conversation_valid_args() -> None:
    # Happy path test for creating a TextMessageConversation with valid arguments
    api_client = CallRail('test_key')
    account_id = 'test_account'
    conversation_data: typing.Dict[str, typing.Any] = {
        'id': 'test_conversation',
        'company_id': 'test_company',
        'initial_tracker_id': 'test_initial_tracker',
        'current_tracker_id': 'test_current_tracker',
        'customer_name': 'John Doe',
        'customer_phone_number': '+1234567890',
        'initial_tracking_number': '+0987654321',
        'current_tracking_number': '+1234567890',
        'last_message_at': dt.datetime.now(),
        'state': 'active',
        'company_time_zone': 'UTC',
        'formatted_customer_phone_number': '(123) 456-7890',
        'formatted_initial_tracking_number': '(098) 765-4321',
        'formatted_current_tracking_number': '(123) 456-7890',
        'formatted_customer_name': 'Doe, John',
        'recent_messages': []
    }

    conversation = TextMessageConversation(api_client, account_id, **conversation_data)

    assert conversation.id == conversation_data['id']
    assert conversation.customer_name == conversation_data['customer_name']
    assert conversation.recent_messages == conversation_data['recent_messages']


# Tests deserializing JSON data into a TextMessageConversation object with missing or invalid fields. 
def test_deserialize_json_missing_fields() -> None:
    # Edge case test for deserializing JSON data into a TextMessageConversation with missing or invalid fields
    api_client = CallRail('test_key')
    account_id = 'test_account'
    json_data = {
        # Missing id field
        'company_id': 'test_company',
        'initial_tracker_id': 'test_initial_tracker',
        'current_tracker_id': 'test_current_tracker',
        'customer_name': 'John Doe',
        'customer_phone_number': '+1234567890',
        'initial_tracking_number': '+0987654321',
        'current_tracking_number': '+1234567890',
        'last_message_at': dt.datetime.now().isoformat(),
        'state': 'active',
        'company_time_zone': 'UTC',
        'formatted_customer_phone_number': '(123) 456-7890',
        'formatted_initial_tracking_number': '(098) 765-4321',
        'formatted_current_tracking_number': '(123) 456-7890',
        'formatted_customer_name': 'Doe, John',
        'recent_messages': []
    }

    with pytest.raises(KeyError):
        TextMessageConversation.from_json(api_client, account_id, json_data)

# Tests deserializing JSON data into a TextMessageConversation object with valid data. 
def test_deserialize_json_valid_data() -> None:
    # Happy path test for deserializing JSON data into a TextMessageConversation with valid data
    api_client = CallRail('test_key')
    account_id = 'test_account'
    json_data = {
        'id': 'test_conversation',
        'company_id': 'test_company',
        'initial_tracker_id': 'test_initial_tracker',
        'current_tracker_id': 'test_current_tracker',
        'customer_name': 'John Doe',
        'customer_phone_number': '+1234567890',
        'initial_tracking_number': '+0987654321',
        'current_tracking_number': '+1234567890',
        'last_message_at': '2022-01-01T00:00:00Z',
        'state': 'active',
        'company_time_zone': 'UTC',
        'formatted_customer_phone_number': '(123) 456-7890',
        'formatted_initial_tracking_number': '(098) 765-4321',
        'formatted_current_tracking_number': '(123) 456-7890',
        'formatted_customer_name': 'Doe, John',
        'recent_messages': [
            {
                'direction': 'incoming',
                'content': 'Hello',
                'created_at': '2022-01-01T00:00:00Z'
            },
            {
                'direction': 'outgoing',
                'content': 'Hi there',
                'created_at': '2022-01-01T00:01:00Z'
            }
        ]
    }

    conversation = TextMessageConversation.from_json(api_client, account_id, json_data)

    assert conversation.id == json_data['id']
    assert conversation.customer_name == json_data['customer_name']
    assert len(conversation.recent_messages) == len(json_data['recent_messages'])

# Tests accessing attributes of a TextMessageConversation object. 
def test_access_attributes() -> None:
    # Happy path test for accessing attributes of a TextMessageConversation object
    api_client = CallRail('test_key')
    account_id = 'test_account'
    conversation_data = {
        'id': 'test_conversation',
        'company_id': 'test_company',
        'initial_tracker_id': 'test_initial_tracker',
        'current_tracker_id': 'test_current_tracker',
        'customer_name': 'John Doe',
        'customer_phone_number': '+1234567890',
        'initial_tracking_number': '+0987654321',
        'current_tracking_number': '+1234567890',
        'last_message_at': dt.datetime.now(),
        'state': 'active',
        'company_time_zone': 'UTC',
        'formatted_customer_phone_number': '(123) 456-7890',
        'formatted_initial_tracking_number': '(098) 765-4321',
        'formatted_current_tracking_number': '(123) 456-7890',
        'formatted_customer_name': 'Doe, John',
        'recent_messages': []
    }

    conversation = TextMessageConversation(api_client, account_id, **conversation_data)

    assert conversation.id == conversation_data['id']
    assert conversation.customer_name == conversation_data['customer_name']
    assert conversation.recent_messages == conversation_data['recent_messages']