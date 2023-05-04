import pytest
import pytest_mock
import requests_mock
import requests

from pycallrail.callrail import CallRail
from pycallrail.objects.accounts import Account
import typing




# Tests that list_accounts method returns a list of Account objects. 
def test_list_accounts_happy_path(requests_mock: requests_mock.Mocker) -> None:
    # Setup
    api_key = 'test_api_key'
    api_client = CallRail(api_key=api_key)
    mock_response: typing.Dict[str, typing.Any] = {
        "page": 1,
        "per_page": 100,
        "total_pages": 1,
        "total_records": 2,
        "accounts": [
            {
                "id": "ACC8154748ae6bd4e278a7cddd38a662f4f",
                "name": "Last Mile Metrics",
                "outbound_recording_enabled": True,
                "hipaa_account": False
            },
            {
                "id": "ACC8154748ae6bd4e278a7cddd38a662d4d",
                "name": "CallRail",
                "outbound_recording_enabled": True,
                "hipaa_account": False
            }
        ]   
    }
    
    requests_mock.get('https://api.callrail.com/v3/a.json', json=mock_response)

    # Execution
    accounts: typing.List[Account] = api_client.list_accounts()

    # Assertion
    assert len(accounts) == 2
    assert accounts[0].id == 'ACC8154748ae6bd4e278a7cddd38a662f4f'
    assert accounts[1].id == 'ACC8154748ae6bd4e278a7cddd38a662d4d'
    assert accounts[0].name == 'Last Mile Metrics'
    assert accounts[1].name == 'CallRail'
    assert accounts[0].outbound_recording_enabled == True
    assert accounts[1].outbound_recording_enabled == True
    assert accounts[0].hipaa_account == False
    assert accounts[1].hipaa_account == False

# Tests that get_account returns an Account object. 
def test_get_account_happy_path(requests_mock: requests_mock.Mocker) -> None:
    # Setup
    api_key = 'test_api_key'
    api_client = CallRail(api_key=api_key)
    mock_response: typing.Dict[str, typing.Any] = {
        "id": "ACC8154748ae6bd4e278a7cddd38a662f4f",
        "name": "Last Mile Metrics",
        "outbound_recording_enabled": True,
        "hipaa_account": False
    }
    
    requests_mock.get('https://api.callrail.com/v3/a/ACC8154748ae6bd4e278a7cddd38a662f4f.json', json=mock_response)

    # Execution
    account: Account = api_client.get_account(account_id='ACC8154748ae6bd4e278a7cddd38a662f4f')

    # Assertion
    assert account.id == 'ACC8154748ae6bd4e278a7cddd38a662f4f'
    assert account.name == 'Last Mile Metrics'
    assert account.outbound_recording_enabled == True
    assert account.hipaa_account == False

# Tests that _post handles missing response_data_key. 
def test__post_edge_case(requests_mock: requests_mock.Mocker) -> None:
    # Setup
    api_key = 'test_api_key'
    cr = CallRail(api_key=api_key)
    data_post: typing.Dict[str, typing.Any] = {
        "caller_id": "+17703334455",
        "business_phone_number": "+14045556666",
        "customer_phone_number": "+14044442233",
        "recording_enabled": True,
        "outbound_greeting_recording_url": "http://www.test.com/greeting.mp3",
        "outbound_greeting_text": "These are not the droids you are looking for."
    }

    mock_response: typing.Dict[str, typing.Any] = {
        "answered": None,
        "business_phone_number": "+19044567899",
        "customer_city": "Atlanta",
        "customer_country": "US",
        "customer_name": None,
        "customer_phone_number": "+14703444700",
        "customer_state": "GA",
        "direction": "outbound",
        "duration": None,
        "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
        "recording": None,
        "recording_duration": None,
        "start_time": "2017-02-22T15:02:24.916-05:00",
        "tracking_phone_number": "+19044567899",
        "voicemail": False
    }
    
    requests_mock.post('https://api.callrail.com/v3/a/12345/calls.json', json=mock_response)

    # Execution
    response: typing.Dict[str, typing.Any] = typing.cast(
        typing.Dict[str, typing.Any], cr._post(endpoint='a/12345', path='calls.json', data=data_post))

    # Assertion
    assert response == mock_response

# Tests that _relative_paginator handles pagination correctly. 
def test__relative_paginator_edge_case(requests_mock: requests_mock.Mocker) -> None:
    # Setup
    api_key = 'test_api_key'
    cr = CallRail(api_key=api_key)
    mock_response_1: typing.Dict[str, typing.Any] = {
        'accounts': [
            {
                'id': '1',
                'name': 'Test Account 1',
                'outbound_recording_enabled': True,
                'hipaa_account': False
            }
        ],
        'has_next_page': True,
        'next_page': 'https://api.callrail.com/v3/a.json?page=2'
    }
    mock_response_2: typing.Dict[str, typing.Any] = {
        'accounts': [
            {
                'id': '2',
                'name': 'Test Account 2',
                'outbound_recording_enabled': False,
                'hipaa_account': True
            }
        ],
        'has_next_page': False
    }
    requests_mock.get('https://api.callrail.com/v3/a.json', json=mock_response_1)
    requests_mock.get('https://api.callrail.com/v3/a.json?page=2', json=mock_response_2)

    # Execution
    response: typing.List[typing.Dict[str, typing.Any]] = cr._relative_paginator(
        response=requests.get('https://api.callrail.com/v3/a.json'), response_data_key='accounts')

    # Assertion
    assert len(response) == 2
    assert response[0]['id'] == '1'
    assert response[1]['id'] == '2'

# Tests handling of invalid API responses. 
def test_list_accounts_general_behavior(requests_mock: requests_mock.Mocker):
    # Setup
    api_key = 'test_api_key'
    cr = CallRail(api_key=api_key)
    mock_response: typing.Dict[str, str] = {
        'error': 'Invalid API key'
    }
    requests_mock.get('https://api.callrail.com/v3/a.json', json=mock_response, status_code=401)

    # Execution and Assertion
    with pytest.raises(requests.exceptions.HTTPError):
        cr.list_accounts()

    # Tests that _get correctly handles query string parameters. 
def test__get_happy_path(requests_mock: requests_mock.Mocker):
    # Setup
    api_key = 'test_api_key'
    cr = CallRail(api_key=api_key)
    mock_response: typing.Dict[str, typing.Any] = {
        "page": 1,
        "per_page": 100,
        "total_pages": 1,
        "total_records": 2,
        "accounts": [
            {
                "id": "ACC8154748ae6bd4e278a7cddd38a662f4f",
                "name": "Last Mile Metrics",
                "outbound_recording_enabled": True,
                "hipaa_account": False
            },
            {
                "id": "ACC8154748ae6bd4e278a7cddd38a662d4d",
                "name": "CallRail",
                "outbound_recording_enabled": True,
                "hipaa_account": False
            }
        ]   
    }

    requests_mock.get('https://api.callrail.com/v3/a.json?sorting=name', json=mock_response)

    # Execution
    response = cr._get(endpoint='a.json', response_data_key='accounts', params={'sorting': 'name'})

    # Assertion
    assert response == mock_response['accounts']

# Tests that _post handles missing response_data_key.  
def test__post_happy_path(requests_mock: requests_mock.Mocker) -> None:
    # Setup
    api_key = 'test_api_key'
    cr = CallRail(api_key=api_key)
    mock_response = {
        'data': {
            'id': 1,
            'name': 'Test Account',
            'outbound_recording_enabled': True,
            'hipaa_account': False
        }
    }

    requests_mock.post('https://api.callrail.com/v3/test_endpoint', json=mock_response)

    # Test
    response = cr._post(endpoint='test_endpoint', response_data_key='data')

    # Assert
    assert response == mock_response['data']
    assert requests_mock.last_request.headers['Authorization'] == f'Token token="{api_key}"'

# Tests handling of API errors and exceptions.  
def test_get_account_general_behavior(requests_mock: requests_mock.Mocker) -> None:
    # Test handling of API errors and exceptions in get_account method
    account_id = '123'
    url = f'https://api.callrail.com/v3/a/{account_id}.json'
    requests_mock.get(url, status_code=404)

    callrail = CallRail(api_key='test')
    with pytest.raises(requests.exceptions.HTTPError):
        callrail.get_account(account_id=account_id)

# Tests handling of unexpected input parameters in CallRail constructor.  
def test_CallRail_constructor_general_behavior() -> None:
    # Test handling of unexpected input parameters in CallRail constructor
    with pytest.raises(TypeError):
        CallRail(api_key='test', invalid_param=True)