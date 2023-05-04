import pytest
import pytest_mock
import requests_mock
import requests

from pycallrail.callrail import CallRail
from pycallrail.objects.calls import Call
import typing
import logging
import datetime as dt

# Tests that a Call object can be created with valid arguments. 
def test_create_call_with_valid_arguments(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    call_data: typing.Dict[str, typing.Any] =  {
        "answered": False,
        "business_phone_number": None,
        "customer_city": "New York City",
        "customer_country": "US",
        "customer_name": "Jimmy Pesto, Sr.",
        "customer_phone_number": "+13036231131",
        "customer_state": "NY",
        "direction": "inbound",
        "duration": 4,
        "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
        "recording": "https://api.callrail.com/v3/a/227799611/calls/111222333/recording.json",
        "recording_duration": "27",
        "recording_player": "https://app.callrail.com/calls/111222333/recording?access_key=3b91eb7f7cc08a4d01ed",
        "start_time": "2017-01-24T11:27:48.119-05:00",
        "tracking_phone_number": "+13038163491",
        "voicemail": False,
        "agent_email": "gil@televised.com"
    }

    # Act
    call = Call(api_client, account_id, **call_data)

    # Assert
    assert call.answered == call_data['answered']
    assert call.customer_city == call_data['customer_city']
    assert call.customer_country == call_data['customer_country']
    assert call.customer_name == call_data['customer_name']
    assert call.customer_phone_number == call_data['customer_phone_number']
    assert call.customer_state == call_data['customer_state']
    assert call.direction == call_data['direction']
    assert call.duration == call_data['duration']
    assert call.id == call_data['id']
    assert call.start_time == call_data['start_time']
    assert call.tracking_phone_number == call_data['tracking_phone_number']
    assert call.voicemail == call_data['voicemail']

# Tests that a Call object can be created with valid arguments. 
def test_call_creation_two_instances(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    call_data: typing.Dict[str, typing.Any] =  {
        "answered": False,
        "business_phone_number": None,
        "customer_city": "New York City",
        "customer_country": "US",
        "customer_name": "Jimmy Pesto, Sr.",
        "customer_phone_number": "+13036231131",
        "customer_state": "NY",
        "direction": "inbound",
        "duration": 4,
        "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
        "recording": "https://api.callrail.com/v3/a/227799611/calls/111222333/recording.json",
        "recording_duration": "27",
        "recording_player": "https://app.callrail.com/calls/111222333/recording?access_key=3b91eb7f7cc08a4d01ed",
        "start_time": "2017-01-24T11:27:48.119-05:00",
        "tracking_phone_number": "+13038163491",
        "voicemail": False,
        "agent_email": "gil@televised.com"
    }

    # Act
    call = Call(api_client, account_id, **call_data)

    call_data_2: typing.Dict[str, typing.Any] =  {
        "answered": True,
        "business_phone_number": None,
        "customer_city": "Toronto",
        "customer_country": "CA",
        "customer_name": "Jimmy Pesto, Sr.",
        "customer_phone_number": "+13036231131",
        "customer_state": "NY",
        "direction": "inbound",
        "duration": 4,
        "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
        "recording": "https://api.callrail.com/v3/a/227799611/calls/111222333/recording.json",
        "recording_duration": "27",
        "recording_player": "https://app.callrail.com/calls/111222333/recording?access_key=3b91eb7f7cc08a4d01ed",
        "start_time": "2017-01-24T11:27:48.119-05:00",
        "tracking_phone_number": "+13038163491",
        "voicemail": False,
        "agent_email": "gil@televised.com"
    }

    call_2 = Call(api_client, account_id, **call_data_2)

    # Assert
    assert call.answered == call_data['answered']
    assert call.customer_city == call_data['customer_city']
    assert call.customer_country == call_data['customer_country']
    assert call.customer_name == call_data['customer_name']
    assert call.customer_phone_number == call_data['customer_phone_number']
    assert call.customer_state == call_data['customer_state']
    assert call.direction == call_data['direction']
    assert call.duration == call_data['duration']
    assert call.id == call_data['id']
    assert call.start_time == call_data['start_time']
    assert call.tracking_phone_number == call_data['tracking_phone_number']
    assert call.voicemail == call_data['voicemail']

    assert call_2.answered == call_data_2['answered']
    assert call_2.customer_city == call_data_2['customer_city']
    assert call_2.customer_country == call_data_2['customer_country']

# Tests that a Call object can be updated with valid arguments. 
def test_update_call_with_valid_arguments(requests_mock: requests_mock.Mocker) -> None:
    # Arrange
    api_client = CallRail(api_key='123')
    account_id = '123'
    
    call_data =  {
        "answered": False,
        "business_phone_number": None,
        "customer_city": "Denver",
        "customer_country": "US",
        "customer_name": "James Smith",
        "customer_phone_number": "+13036231131",
        "customer_state": "CO",
        "direction": "inbound",
        "duration": 4,
        "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
        "recording": "https://api.callrail.com/v3/a/227799611/calls/213472384/recording.json",
        "recording_duration": "27",
        "start_time": "2017-01-24T11:27:48.119-05:00",
        "tracking_phone_number": "+13038163491",
        "voicemail": False
    }

    call = Call(api_client, account_id, **call_data)

    update_data = {
        "note": "Call customer back tomorrow",
        "tags": ["New Client"],
        "lead_status": "good_lead",
        "value": "$1.00",
        "append_tags": True,
        "customer_name": "James Smith"
    }

    # Act
    requests_mock.put(
        url=f'https://api.callrail.com/v3/a/{account_id}/calls/{call.id}.json',
        json= call_data 
    )


    call.update(
        tags = update_data['tags'], 
        note = update_data['note'], 
        value = update_data['value'], 
        append_tags = update_data['append_tags'], 
        customer_name = update_data['customer_name'])

    # Assert
    assert call.tags == update_data['tags']
    assert call.note == update_data['note']
    assert call.value == update_data['value']
    assert call.customer_name == update_data['customer_name']

# Tests that a Call object cannot be created with missing or invalid required arguments. 
def test_create_call_with_invalid_arguments(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    call_data = {
        "answered": False,
        "business_phone_number": None,
        "customer_city": "Denver",
        "customer_country": "US",
        "customer_name": "James Smith",
        "customer_phone_number": "+13036231131",
        "customer_state": "CO",
        "direction": "inbound",
        "duration": 4,
        "recording": "https://api.callrail.com/v3/a/227799611/calls/213472384/recording.json",
        "recording_duration": "27",
        "start_time": "2017-01-24T11:27:48.119-05:00",
        "tracking_phone_number": "+13038163491",
        "invalid_argument": True
    } 

    # Act & Assert
    with pytest.raises(AttributeError):
        Call(api_client, account_id, **call_data)

def test_update_call_with_invalid_arguments(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    call_data = {
        "answered": False,
        "business_phone_number": None,
        "customer_city": "Denver",
        "customer_country": "US",
        "customer_name": "James Smith",
        "customer_phone_number": "+13036231131",
        "customer_state": "CO",
        "direction": "inbound",
        "duration": 4,
        "recording": "https://api.callrail.com/v3/a/227799611/calls/213472384/recording.json",
        "recording_duration": "27",
        "start_time": "2017-01-24T11:27:48.119-05:00",
        "tracking_phone_number": "+13038163491"
    }

    call = Call(api_client, account_id, **call_data)

    with pytest.raises(Exception):
        call.update(invalid_argument = True)

# Tests that the recording of a call can be retrieved with a valid recording URL. 
def test_get_recording_with_valid_recording_url(requests_mock: requests_mock.Mocker) -> None:
    # Arrange
    api_client = CallRail(api_key='123')
    account_id = '123'
    call_data = {
        'answered': True,
        'customer_city': 'New York',
        'customer_country': 'USA',
        'customer_name': 'John Doe',
        'customer_phone_number': '123-456-7890',
        'customer_state': 'NY',
        'direction': 'inbound',
        'duration': 60,
        'id': '456',
        'start_time': '2017-01-24T11:27:48.119-05:00',
        'tracking_phone_number': '987-654-3210',
        'voicemail': False,
        'recording': 'http://example.com/recording.mp3'
    }
    call = Call(api_client, account_id, **call_data)
    recording_content = b'This is a recording'

    # Mock the response from the recording URL
    requests_mock.get(
        url='http://example.com/recording.mp3',
        content=recording_content
    )

    # Act
    recording = call.get_recording()

    # Assert
    assert recording == recording_content

# Tests that None is returned when attempting to retrieve the recording of a call with no recording URL. 
def test_get_recording_with_no_recording_url(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    call_data = {
        'answered': True,
        'customer_city': 'New York',
        'customer_country': 'USA',
        'customer_name': 'John Doe',
        'customer_phone_number': '123-456-7890',
        'customer_state': 'NY',
        'direction': 'inbound',
        'duration': 60,
        'id': '456',
        'start_time': '2017-01-24T11:27:48.119-05:00',
        'tracking_phone_number': '987-654-3210',
        'voicemail': False,
        'recording': None
    }
    call = Call(api_client, account_id, **call_data)

    # Act
    recording = call.get_recording()

    # Assert
    assert recording is None

# Tests that JSON data can be successfully deserialized to a Call object.  
def test_deserialize_json_data_to_call_object(mocker: pytest_mock.MockerFixture) -> None:
    # Setup
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    json_data = {
        'answered': True,
        'business_phone_number': '555-555-5555',
        'customer_city': 'New York',
        'customer_country': 'USA',
        'customer_name': 'John Doe',
        'customer_phone_number': '555-555-5555',
        'customer_state': 'NY',
        'direction': 'inbound',
        'duration': 60,
        'id': '456',
        'recording': 'http://example.com/recording.mp3',
        'recording_duration': '00:01:00',
        'recording_player': 'http://example.com/recording_player.mp3',
        'start_time': '2022-01-01T00:00:00Z',
        'tracking_phone_number': '555-555-5555',
        'voicemail': False,
        'call_type': 'sales',
        'company_id': '789',
        'company_name': 'Acme Inc.',
        'company_time_zone': 'America/New_York',
        'created_at': '2022-01-01T00:00:00Z',
        'device_type': 'mobile',
        'first_call': True,
        'formatted_call_type': 'Sales Call',
        'formatted_customer_location': 'New York, NY, USA',
        'formatted_business_phone_number': '(555) 555-5555',
        'formatted_customer_name': 'John Doe',
        'prior_calls': 2,
        'formatted_customer_name_or_phone_number': '(555) 555-5555',
        'formatted_customer_phone_number': '(555) 555-5555',
        'formatted_duration': '1m 0s',
        'formatted_tracking_phone_number': '(555) 555-5555',
        'formatted_tracking_source': 'Google Ads',
        'formatted_value': '$100',
        'good_lead_call_id': 123,
        'good_lead_call_time': '2022-01-01T00:00:00Z',
        'lead_status': 'qualified',
        'note': 'This was a good call.',
        'source': 'google',
        'source_name': 'Google Ads',
        'tags': ['tag1', 'tag2'],
        'total_calls': 10,
        'value': 100,
        'waveforms': [{'time': 0, 'value': 0}, {'time': 1, 'value': 1}],
        'tracker_id': 'abc123',
        'speaker_percent': {'speaker1': 50, 'speaker2': 50},
        'keywords': 'important keywords',
        'medium': 'cpc',
        'campaign': 'campaign1',
        'referring_url': 'http://example.com/referrer',
        'landing_page_url': 'http://example.com/landing',
        'last_requested_url': 'http://example.com/requested',
        'referrer_domain': 'example.com',
        'utm_source': 'google',
        'utm_medium': 'cpc',
        'utm_term': 'term1',
        'utm_content': 'content1',
        'utm_campaign': 'campaign1',
        'utma': '123456789.1234567890.1234567890.1234567890.1',
        'utmb': '123456789.1.10.1234567890',
        'utmc': '',
        'utmv': '',
        'utmz': '',
        'ga': '',
        'gclid': '',
        'fbclid': '',
        'msclkid': '',
        'milestones': {'milestone1': '2022-01-01T00:00:00Z', 'milestone2': '2022-01-01T00:01:00Z'},
        'timeline_url': 'http://example.com/timeline',
        'keywords_spotted': ['keyword1', 'keyword2'],
        'call_highlights': [{'start_time': '2022-01-01T00:00:00Z', 'end_time': '2022-01-01T00:01:00Z', 'text': 'highlighted text'}],
        'agent_email': 'johndoe@example.com',
        'keypad_entries': {'1': 2, '2': 3}
    }

    # Exercise
    call = Call.from_json(api_client, account_id, json_data)

    # Verify
    assert isinstance(call, Call)
    assert call.answered == True
    assert call.business_phone_number == '555-555-5555'
    assert call.customer_city == 'New York'
    assert call.customer_country == 'USA'
    assert call.customer_name == 'John Doe'
    assert call.customer_phone_number == '555-555-5555'
    assert call.customer_state == 'NY'
    assert call.direction == 'inbound'
    assert call.duration == 60
    assert call.id == '456'
    assert call.recording == 'http://example.com/recording.mp3'
    assert call.recording_duration == '00:01:00'
    assert call.recording_player == 'http://example.com/recording_player.mp3'
    assert isinstance(call.start_time, dt.datetime)
    assert call.start_time.isoformat() == '2022-01-01T00:00:00+00:00'
    assert call.tracking_phone_number == '555-555-5555'
    assert call.voicemail == False
    assert call.call_type == 'sales'
    assert call.company_id == '789'
    assert call.company_name == 'Acme Inc.'
    assert call.company_time_zone == 'America/New_York'
    assert call.created_at == '2022-01-01T00:00:00Z'
    assert call.device_type == 'mobile'
    assert call.first_call == True
    assert call.formatted_call_type == 'Sales Call'
    assert call.formatted_customer_location == 'New York, NY, USA'
    assert call.formatted_business_phone_number == '(555) 555-5555'
    assert call.formatted_customer_name == 'John Doe'
    assert call.prior_calls == 2
    assert call.formatted_customer_name_or_phone_number == '(555) 555-5555'
    assert call.formatted_customer_phone_number == '(555) 555-5555'
    assert call.formatted_duration == '1m 0s'
    assert call.formatted_tracking_phone_number == '(555) 555-5555'
    assert call.formatted_tracking_source == 'Google Ads'
    assert call.formatted_value == '$100'
    assert call.good_lead_call_id == 123
    assert call.good_lead_call_time == '2022-01-01T00:00:00Z'
    assert call.lead_status == 'qualified'
    assert call.note == 'This was a good call.'
    assert call.source == 'google'
    assert call.source_name == 'Google Ads'
    assert call.tags == ['tag1', 'tag2']
    assert call.total_calls == 10
    assert call.value == 100
    assert isinstance(call.waveforms, list)
    assert call.waveforms == [{'time': 0, 'value': 0}, {'time': 1, 'value': 1}]
    assert call.tracker_id == 'abc123'
    assert call.speaker_percent == {'speaker1': 50, 'speaker2': 50}
    assert call.keywords == 'important keywords'
    assert call.medium == 'cpc'
    assert call.campaign == 'campaign1'
    assert call.referring_url == 'http://example.com/referrer'
    assert call.landing_page_url == 'http://example.com/landing'
    assert call.last_requested_url == 'http://example.com/requested'
    assert call.referrer_domain == 'example.com'
    assert call.utm_source == 'google'
    assert call.utm_medium == 'cpc'
    assert call.utm_term == 'term1'
    assert call.utm_content == 'content1'
    assert call.utm_campaign == 'campaign1'
    assert call.utma == '123456789.1234567890.1234567890.1234567890.1'
    assert call.utmb == '123456789.1.10.1234567890'
    assert call.utmc == ''
    assert call.utmv == ''
    assert call.utmz == ''
    assert call.ga == ''
    assert call.gclid == ''
    assert call.fbclid == ''
    assert call.msclkid == ''
    assert isinstance(call.milestones, dict)
    assert call.milestones == {'milestone1': '2022-01-01T00:00:00Z', 'milestone2': '2022-01-01T00:01:00Z'}
    assert call.timeline_url == 'http://example.com/timeline'
    assert call.keywords_spotted == ['keyword1', 'keyword2']
    assert isinstance(call.call_highlights, list)
    assert call.call_highlights == [{'start_time': '2022-01-01T00:00:00Z', 'end_time': '2022-01-01T00:01:00Z', 'text': 'highlighted text'}]
    assert call.agent_email == 'johndoe@example.com'
    assert isinstance(call.keypad_entries, dict)
    assert call.keypad_entries == {'1': 2, '2': 3}