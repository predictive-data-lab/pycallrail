import pytest
from unittest.mock import patch, MagicMock
from pytest_mock import MockerFixture
from requests_mock.mocker import Mocker
from pycallrail.callrail import CallRail, PaginationType
from pycallrail.api.accounts import Account
from requests import Response
from typing import Union, Generator
import requests_mock
import requests
from requests_mock.adapter import Adapter

# Tests that the list_accounts method returns a list of Account objects when given valid parameters. 
# Tests that the list_accounts() function successfully lists all accounts for the authenticated user. 
def test_list_accounts_happy_path(requests_mock: Mocker):
    """
    Tests that the list_accounts() function successfully lists all accounts for the authenticated user.
    """
    # Set up mock response
    requests_mock.get(
        "https://api.callrail.com/v3/a.json",
        json={
            "accounts": [
                {
                    "id": 1,
                    "name": "Test Account 1"
                },
                {
                    "id": 2,
                    "name": "Test Account 2"
                }
            ]
        },
        status_code=200
    )

    # Initialize CallRail object and call list_accounts()
    cr = CallRail(api_key="test_api_key")
    accounts: list[Account] = cr.list_accounts()

    # Assert that the correct number of accounts were returned
    assert len(accounts) == 2

    # Assert that each account is an instance of the Account class
    for account in accounts:
        assert isinstance(account, Account)
    
# Tests that the get_account() function successfully gets a single account. 
def test_get_account_happy_path(requests_mock: Mocker):
    """
    Tests that the get_account() function successfully gets a single account.
    """
    # Set up mock response
    requests_mock.get(
        "https://api.callrail.com/v3/a/1.json",
        json={
            "account": {
                "id": 1,
                "name": "Test Account 1"
            }
        },
        status_code=200
    )

    # Initialize CallRail object and call get_account()
    cr = CallRail(api_key="test_api_key")
    account: Account = cr.get_account(account_id=1)

    # Assert that the returned account is an instance of the Account class
    assert isinstance(account, Account)

# Tests that the list_accounts() function handles an error response from the API. 
def test_list_accounts_error_response(requests_mock: Mocker):
    """
    Tests that the list_accounts() function handles an error response from the API.
    """
    # Set up mock response
    requests_mock.get(
        "https://api.callrail.com/v3/a.json",
        json={
            "error": "Invalid API key"
        },
        status_code=401
    )

    # Initialize CallRail object and call list_accounts()
    cr = CallRail(api_key="invalid_api_key")
    
    with pytest.raises(Exception):
        cr.list_accounts()

# Tests that the list_accounts() function handles an empty response from the API. 
def test_list_accounts_empty_response(requests_mock: Mocker):
    """
    Tests that the list_accounts() function handles an empty response from the API.
    """
    # Set up mock response
    requests_mock.get(
        "https://api.callrail.com/v3/a.json",
        json={},
        status_code=200
    )

    # Initialize CallRail object and call list_accounts()
    cr = CallRail(api_key="test_api_key")
    
    with pytest.raises(AttributeError):
        cr.list_accounts()
    
    # Tests the base GET, POST, PUT, and DELETE request functions. 
def test_base_request_functions(requests_mock: Mocker):
    """
    Tests the base GET, POST, PUT, and DELETE request functions.
    """
    # Set up mock responses
    requests_mock.get(
        "https://api.callrail.com/v3/test_endpoint.json",
        json={
            "data": [
                {
                    "id": 1,
                    "name": "Test 1"
                },
                {
                    "id": 2,
                    "name": "Test 2"
                }
            ]
        },
        status_code=200
    )
    requests_mock.post(
        "https://api.callrail.com/v3/test_endpoint.json",
        json={
            "data": {
                "id": 3,
                "name": "Test 3"
            }
        },
        status_code=201
    )
    requests_mock.put(
        "https://api.callrail.com/v3/test_endpoint/1.json",
        json={
            "data": {
                "id": 1,
                "name": "Updated Test 1"
            }
        },
        status_code=200
    )
    requests_mock.delete(
        "https://api.callrail.com/v3/test_endpoint/1.json",
        status_code=204
    )

    # Initialize CallRail object and call base request functions
    cr = CallRail(api_key="test_api_key")
    get_response = cr._get(endpoint="test_endpoint.json")
    post_response = cr._post(endpoint="test_endpoint.json")
    put_response = cr._put(endpoint="test_endpoint", path="1.json")
    delete_response = cr._delete(endpoint="test_endpoint", path="/1.json")

    # Assert that the responses are as expected
    assert len(get_response['data']) == 2
    assert post_response['data']["name"] == "Test 3"
    assert put_response['data']["name"] == "Updated Test 1"
    assert delete_response is None

# Tests the base relative pagination function. 
def test_relative_pagination_function(requests_mock: Mocker):
    """
    Tests the base relative pagination function.
    """
    # Set up mock responses
    requests_mock.get(
        "https://api.callrail.com/v3/test_endpoint.json",
        json={
            "data": [
                {
                    "id": 1,
                    "name": "Test 1"
                },
                {
                    "id": 2,
                    "name": "Test 2"
                }
            ],
            "next_page": "https://api.callrail.com/v3/test_endpoint?page=2",
            "has_next_page": True
        },
        status_code=200
    )
    requests_mock.get(
        "https://api.callrail.com/v3/test_endpoint?page=2",
        json={
            "data": [
                {
                    "id": 3,
                    "name": "Test 3"
                },
                {
                    "id": 4,
                    "name": "Test 4"
                }
            ],
            "next_page": None,
            "has_next_page": False
        },
        status_code=200
    )

    # Initialize CallRail object and call relative pagination function
    cr = CallRail(api_key="test_api_key")

    initial_response = requests.get("https://api.callrail.com/v3/test_endpoint.json")

    response = cr._relative_paginator(response=initial_response, response_data_key='data')

    # Assert that the response is as expected
    assert len(response) == 4

# Tests the base offset pagination function.  
def test_offset_pagination_function(requests_mock: Mocker):
    """
    Tests the base offset pagination function.
    """
    # Set up mock responses
    first_page_response = {
        "data": [
            {
                "id": 1,
                "name": "Test 1"
            },
            {
                "id": 2,
                "name": "Test 2"
            }
        ],
        "page": 1,
        "total_pages": 2
    }
    second_page_response = {
        "data": [
            {
                "id": 3,
                "name": "Test 3"
            },
            {
                "id": 4,
                "name": "Test 4"
            }
        ],
        "page": 2,
        "total_pages": 2
    }

    requests_mock.get(
        "https://api.callrail.com/v3/test_endpoint.json",
        json=first_page_response,
        status_code=200
    )
    requests_mock.get(
        "https://api.callrail.com/v3/test_endpoint.json?page=2",
        json=second_page_response,
        status_code=200
    )

    first_response = requests.get("https://api.callrail.com/v3/test_endpoint.json")

    # Initialize CallRail instance
    callrail = CallRail(api_key="test_api_key")

    # Test the _offset_paginator function
    response = callrail._offset_paginator(response=first_response, response_data_key='data')

    # Check if the response is a list and has the correct length
    assert isinstance(response, list)
    assert len(response) == 4

    # Check if the response contains the correct data
    expected_data = first_page_response["data"] + second_page_response["data"]
    for i in range(len(response)):
        assert response[i] == expected_data[i]