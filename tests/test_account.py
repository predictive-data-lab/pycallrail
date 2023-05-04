import pytest
import pytest_mock
import requests_mock
import requests

from pycallrail.callrail import CallRail
from pycallrail.objects.textmessages import TextMessage, TextMessageConversation
from pycallrail.objects.accounts import Account
from pycallrail.objects.companies import Company
from pycallrail.objects.calls import Call
import typing
import logging
import datetime as dt
import typeguard
import dataclasses

# Tests that calls can be successNoney listed with various keyword arguments. 
def test_list_calls(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = CallRail('test_key')
    account = Account(api_client, 'test_id', 'test_name', True, False)
    mocker.patch.object(api_client, '_get', return_value=[
        {
        "answered": False,
        "business_phone_number": None,
        "customer_city": "Denver",
        "customer_country": "US",
        "customer_name": "RUEGSEGGER SIMO",
        "customer_phone_number": "+13036231131",
        "customer_state": "CO",
        "direction": "inbound",
        "duration": 60,
        "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
        "recording": "https://api.callrail.com/v3/a/227799611/calls/111222333/recording.json",
        "recording_duration": "27",
        "recording_player": "https://app.callrail.com/calls/111222333/recording?access_key=3b91eb7f7cc08a4d01ed",
        "start_time": "2017-01-24T11:27:48.119-05:00",
        "tracking_phone_number": "+13038163491",
        "voicemail": False,
        "agent_email": "gil@televised.com"
        },
        {
        "answered": False,
        "business_phone_number": None,
        "customer_city": "Blue Ridge",
        "customer_country": "US",
        "customer_name": "BLUE RIDGE, GA",
        "customer_phone_number": "+17064558047",
        "customer_state": "GA",
        "direction": "inbound",
        "duration": 120,
        "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
        "recording": None,
        "recording_duration": None,
        "recording_player": None,
        "start_time": "2017-01-24T19:50:03.456-05:00",
        "tracking_phone_number": "+17708243899",
        "voicemail": False,
        "agent_email": "elbert@bpp.com"
        }
    ])

    # Act
    calls: typing.List[Call] = typing.cast(typing.List[Call],
            account.list_calls(pagination_type='RELATIVE', sorting='duration', filtering={'status': 'completed'})
    )

    # Assert
    assert len(calls) == 2
    assert calls[0].id == 'CAL8154748ae6bd4e278a7cddd38a662f4f'
    assert calls[0].duration == 60
    assert calls[1].id == 'CAL8154748ae6bd4e278a7cddd38a662f4f'
    assert calls[1].duration == 120

# Tests that a single call can be successNoney retrieved with optional field selection. 
def test_get_call(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = CallRail('test_key')
    account = Account(api_client, 'test_id', 'test_name', True, False)
    mocker.patch.object(api_client, '_get', return_value={
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
    })

    # Act
    call = account.get_call('1')

    # Assert
    assert call.id == 'CAL8154748ae6bd4e278a7cddd38a662f4f'
    assert call.duration == 4

# Tests that a call can be successNoney created with various optional parameters. 
def test_create_call(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = CallRail('test_key')
    account = Account(api_client, 'test_id', 'test_name', True, False)
    mocker.patch.object(api_client, '_post', return_value={
        'id': '1', 
        'duration': 60, 
        'start_time': '2017-01-24T11:27:48.119-05:00'})


    # Act
    call: Call = account.create_call(1234567890, '555-555-5555', '444-444-4444', recording_enabled=True)

    # Assert
    assert call.id == '1'
    assert call.duration == 60

# Tests that a tag can be successNoney created with various optional parameters, and that missing required parameters raise a ValueError. 
def test_create_tag(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = CallRail('test_key')
    account = Account(api_client, 'test_id', 'test_name', True, False)
    mocker.patch.object(api_client, '_post', return_value={
    "id": "1234569",
    "name": "Existing Customer",
    "tag_level": "company",
    "color": "gray1",
    "background_color": "gray1",
    "company_id": "COM8154748ae6bd4e278a7cddd38a662f4f",
    "status": "enabled",
    "created_at": "2014-06-06T12:11:02.964-04:00"
    })

    # Act
    tag = account.create_tag(
        name='Existing Customer',
        company_id='COM8154748ae6bd4e278a7cddd38a662f4f',
        tag_level='company',
        color='gray1'
    )

    # Assert
    assert tag.id == '1234569'
    assert tag.name == 'Existing Customer'


    # Act/Assert - Test missing required parameter
    with pytest.raises(ValueError):
        account.create_tag(None)

# Tests that companies can be successNoney listed with various keyword arguments, and that invalid filtering fields raise a ValueError. 
def test_list_companies(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = CallRail('test_key')
    account = Account(api_client, 'test_id', 'test_name', True, False)
    returnval = [
        {
            "id": "COM8154748ae6bd4e278a7cddd38a662f4f",
            "name": "Widget Shop",
            "status": "active",
            "time_zone": "America/New_York",
            "created_at": "2016-06-06T07:06:01.000Z",
            "disabled_at": None,
            "dni_active": True,
            "script_url": "//cdn.callrail.com/companies/183570817/5706dbe6dc972c634a65/12/swap.js",
            "callscribe_enabled": False,
            "lead_scoring_enabled": True,
            "swap_exclude_jquery": None,
            "swap_ppc_override": None,
            "swap_landing_override": None,
            "swap_cookie_duration": 365,
            "callscore_enabled": False,
            "keyword_spotting_enabled": False,
            "form_capture": True
    },
    {
        "id": "COM8154748ae6bd4e278a7cddd38a662f4f",
        "name": "Bob's Burger",
        "status": "active",
        "time_zone": "America/New_York",
        "created_at": "2017-06-20T09:30:08.676Z",
        "disabled_at": None,
        "dni_active": False,
        "script_url": "//cdn.callrail.com/companies/411892629/1dbf0fc11eabdc04483a/12/swap.js",
        "callscribe_enabled": False,
        "lead_scoring_enabled": True,
        "swap_exclude_jquery": None,
        "swap_ppc_override": None,
        "swap_landing_override": None,
        "swap_cookie_duration": 365,
        "callscore_enabled": False,
        "keyword_spotting_enabled": False,
        "form_capture": True
    },
    {
        "id": "COM8154748ae6bd4e278a7cddd38a662f4f",
        "name": "Joe's Icecream",
        "status": "active",
        "time_zone": "America/New_York",
        "created_at": "2016-06-06T07:06:01.000Z",
        "disabled_at": None,
        "dni_active": None,
        "script_url": "//cdn.callrail.com/companies/785622206/81fbf538633804b8dea6/12/swap.js",
        "callscribe_enabled": False,
        "lead_scoring_enabled": True,
        "swap_exclude_jquery": None,
        "swap_ppc_override": None,
        "swap_landing_override": None,
        "swap_cookie_duration": 365,
        "callscore_enabled": False,
        "keyword_spotting_enabled": False,
        "form_capture": False
    }]
    mocker.patch.object(api_client, '_get', return_value=returnval)

    companies = account.list_companies(
        pagination_type='OFFSET', 
        sorting='name', 
        filtering={'status': 'active'})

    # Assert
    assert len(companies) == 3
    assert companies[0].id == 'COM8154748ae6bd4e278a7cddd38a662f4f'
    assert companies[0].name == 'Widget Shop'
    assert companies[1].id == 'COM8154748ae6bd4e278a7cddd38a662f4f'
    assert companies[1].name == 'Bob\'s Burger'
    assert companies[2].id == 'COM8154748ae6bd4e278a7cddd38a662f4f'
    assert companies[2].name == 'Joe\'s Icecream'

    # Act/Assert - Test invalid filtering field
    with pytest.raises(ValueError):
        account.list_companies(filtering={'invalid_field': 'value'})

# Tests that tags can be successNoney listed with various keyword arguments. 
def test_list_tags(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = CallRail('test_key')
    account = Account(api_client, 'test_id', 'test_name', True, False)
    return_val = [
    {
      "id": 993186,
      "name": "Conversion",
      "tag_level": "company",
      "color": "gray1",
      "background_color": "green2",
      "company_id": "COM37221d54e80c4216898d2f857fc69fa0",
      "status": "enabled",
      "created_at": "2017-07-24T11:13:47.366-04:00"
    },
    {
      "id": 1932597,
      "name": "Sales",
      "tag_level": "company",
      "color": "gray1",
      "background_color": "blue2",
      "company_id": "COM37221d54e80c4216898d2f857fc69fa0",
      "status": "enabled",
      "created_at": "2019-04-05T13:38:36.258-04:00"
    },
    {
      "id": 2672419,
      "name": "Unanswered",
      "tag_level": "company",
      "color": "gray1",
      "background_color": "yellow1",
      "company_id": "COM37221d54e80c4216898d2f857fc69fa0",
      "status": "enabled",
      "created_at": "2020-10-16T16:07:35.554-04:00"
    }
  ]
    mocker.patch.object(api_client, '_get', return_value=return_val)

    # Act
    tags = account.list_tags(pagination_type='ABSOLUTE', sorting='name', filtering={'status': 'active'})

    # Assert
    assert len(tags) == 3
    assert tags[0].id == 993186
    assert tags[0].name == 'Conversion'
    assert tags[1].id == 1932597
    assert tags[1].name == 'Sales'
    assert tags[2].id == 2672419
    assert tags[2].name == 'Unanswered'

# Tests that a single company can be successNoney retrieved with optional field selection.  
def test_get_company(mocker: pytest_mock.MockerFixture):
    # Arrange
    api_client = CallRail('test_key')
    account = Account(api_client, 'test_id', 'test_name', True, False)
    company_id = 'COM8154748ae6bd4e278a7cddd38a662f4f'
    expected_url = f'a/{account.id}'
    expected_path = f'companies/{company_id}.json'
    expected_data = {
        "id": "COM8154748ae6bd4e278a7cddd38a662f4f",
        "name": "Widget Shop",
        "status": "active",
        "time_zone": "America/New_York",
        "created_at": "2016-06-06T07:06:01.000Z",
        "disabled_at": None,
        "dni_active": True,
        "script_url": "//cdn.callrail.com/companies/183570817/5706dbe6dc972c634a65/12/swap.js",
        "callscore_enabled": False,
        "lead_scoring_enabled": True,
        "swap_exclude_jquery": None,
        "swap_ppc_override": None,
        "swap_landing_override": None,
        "swap_cookie_duration": 365,
        "callscribe_enabled": False,
        "keyword_spotting_enabled": False,
        "form_capture": True,
    }
    mocker.patch.object(api_client, '_get', return_value=expected_data)

    # Act
    company: Company = account.get_company(company_id)

    # Assert
    api_client._get.assert_called_once_with(endpoint=expected_url, path=expected_path)
    assert isinstance(company, Company)
    assert company.id == company_id
    assert company.name == 'Widget Shop'

# Tests that a company can be successNoney created with various optional parameters.  
def test_create_company(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = CallRail('test_key')
    account = Account(api_client, 'test_id', 'test_name', True, False)
    expected_url = f'a/{account.id}'
    expected_path = f'companies.json'
    
    expected_data = {
        "id": "COM8154748ae6bd4e278a7cddd38a662f4f",
        "name": "Widget Shop",
        "status": "active",
        "time_zone": "America/New_York",
        "created_at": "2017-01-26T22:58:04.184Z",
        "disabled_at": None,
        "dni_active": None,
        "script_url": "//cdn.callrail.com/companies/279054151/a74c824140d67442debd/12/swap.js",
        "callscribe_enabled": False,
        "lead_scoring_enabled": False,
        "swap_exclude_jquery": None,
        "swap_ppc_override": None,
        "swap_landing_override": None,
        "swap_cookie_duration": 365,
        "callscore_enabled": False,
        "keyword_spotting_enabled": False
    }

    mocker.patch.object(api_client, '_post', return_value=expected_data)

    # Act
    company = account.create_company(name='Widget Shop', time_zone='America/New_York')

    # Assert
    api_client._post.assert_called_once_with(endpoint=expected_url, path=expected_path, data={'name': 'Widget Shop', 'time_zone': 'America/New_York'})
    assert isinstance(company, Company)
    assert company.id == 'COM8154748ae6bd4e278a7cddd38a662f4f'
    assert company.name == 'Widget Shop'

    # Tests that text message conversations can be successfully listed with various keyword arguments.  
def test_list_text_message_conversations(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = CallRail('test_key')
    account = Account(api_client, 'test_id', 'test_name', True, False)
    expected_url = f'a/{account.id}'
    expected_path = f'text-messages.json'
    expected_data = [
    {
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
    },
    {
      "id": "KZaGY",
      "company_id": "COM8154748ae6bd4e278a7cddd38a662f4f",
      "initial_tracker_id": "TRK8154748ae6bd4e278a7cddd38a662f4f",
      "current_tracker_id": "TRK8154748ae6bd4e278a7cddd38a662f4f",
      "customer_name": "POWELL ANDY",
      "customer_phone_number": "+14042223333",
      "initial_tracking_number": "+14045556677",
      "current_tracking_number": "+17703334455",
      "last_message_at": "2016-07-28T19:26:43.578Z",
      "state": "active",
      "company_time_zone": "America/New_York",
      "formatted_customer_phone_number": "404-222-3333",
      "formatted_initial_tracking_number": "404-555-6677",
      "formatted_current_tracking_number": "770-333-4455",
      "formatted_customer_name": "Powell Andy",
      "recent_messages": [
        {
          "direction": "outgoing",
          "content": "It’s not impossible. I used to bullseye womp rats in my T-16 back home, they’re not much bigger than two meters.",
          "created_at": "2016-07-28T19:28:21.578Z"
        },
        {
          "direction": "incoming",
          "content": "That's impossible, even for a computer!",
          "created_at": "2016-07-28T19:26:43.578Z"
        }
      ]
    }
  ]


    mocker.patch.object(api_client, '_get', return_value=expected_data)

    # Act
    conversations = account.list_text_message_conversations()

    # Assert
    api_client._get.assert_called_once_with(
        endpoint=expected_url, 
        path=expected_path, 
        params=None, 
        response_data_key='conversations',
        pagination_type='RELATIVE'
    )

    assert isinstance(conversations, list)
    assert len(conversations) == 2
    assert isinstance(conversations[0], TextMessageConversation)
    assert isinstance(conversations[1], TextMessageConversation)
    assert conversations[0].id == 'KZaGR'
    assert conversations[1].id == 'KZaGY'
    assert conversations[0].company_id == 'COM8154748ae6bd4e278a7cddd38a662f4f'
    assert conversations[1].company_id == 'COM8154748ae6bd4e278a7cddd38a662f4f'
    assert conversations[0].initial_tracker_id == 'TRK8154748ae6bd4e278a7cddd38a662f4f'
    assert conversations[1].initial_tracker_id == 'TRK8154748ae6bd4e278a7cddd38a662f4f'

    # assert text messages were created
    assert isinstance(conversations[0].recent_messages[0], TextMessage)
    assert conversations[0].recent_messages[0].content == 'Awww! But I was going into Tosche Station to pick up some power converters!'
    assert isinstance(conversations[0].recent_messages[1], TextMessage)
    assert conversations[0].recent_messages[1].content == 'Take these two over to the garage, will you?  I want them cleaned up before dinner.'