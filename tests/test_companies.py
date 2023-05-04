import pytest
import pytest_mock
import requests_mock
import requests

from pycallrail.callrail import CallRail
from pycallrail.objects.companies import Company
import typing
import logging
import datetime as dt

# Tests creating a Company object with valid parameters. 
def test_create_company_valid_params(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    company_data = {
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

    # Act
    company = Company(api_client, account_id, **company_data)

    # Assert
    assert company.id == company_data['id']
    assert company.name == company_data['name']
    assert company.status == company_data['status']
    assert company.time_zone == company_data['time_zone']
    assert company.created_at == company_data['created_at']
    assert company.disabled_at == company_data['disabled_at']
    assert company.dni_active == company_data['dni_active']
    assert company.script_url == company_data['script_url']
    assert company.callscore_enabled == company_data['callscore_enabled']
    assert company.lead_scoring_enabled == company_data['lead_scoring_enabled']
    assert company.swap_exclude_jquery == company_data['swap_exclude_jquery']
    assert company.swap_ppc_override == company_data['swap_ppc_override']
    assert company.swap_landing_override == company_data['swap_landing_override']
    assert company.swap_cookie_duration == company_data['swap_cookie_duration']
    assert company.callscribe_enabled == company_data['callscribe_enabled']
    assert company.keyword_spotting_enabled == company_data['keyword_spotting_enabled']

# Tests updating a Company object with valid parameters. 
def test_update_company_valid_params(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    company_data = {
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
    company = Company(api_client, account_id, **company_data)

    updated_name = 'Updated Company Name'

    # Act
    company.update(name=updated_name)

    # Assert
    assert company.name == updated_name

# Tests creating a Company object with missing parameters. 
def test_create_company_missing_params(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    # Act and Assert
    with pytest.raises(TypeError):
        Company(api_client, account_id)

# Tests creating a Company object with invalid parameters. 
def test_create_company_invalid_params(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock()
    account_id = '123'

    # Act and Assert
    with pytest.raises(AttributeError):
        Company(api_client, account_id, invalid_param='invalid')

# Tests deleting a Company object successfully. 
def test_delete_company(mocker: pytest_mock.MockerFixture):
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    company_data = {
        'id': '456',
        'name': 'Test Company',
        'status': 'active',
        'time_zone': 'America/New_York',
        'created_at': dt.datetime.now(),
        'disabled_at': None,
        'dni_active': False,
        'script_url': 'https://example.com/script.js',
        'callscore_enabled': True,
        'lead_scoring_enabled': False,
        'swap_exclude_jquery': None,
        'swap_ppc_override': None,
        'swap_landing_override': None,
        'swap_cookie_duration': None,
        'callscribe_enabled': True,
        'keyword_spotting_enabled': None,
        'form_capture': True
    }
    company = Company(api_client, account_id, **company_data)

    # Act
    company.delete()

    # Assert
    api_client._delete.assert_called_once_with(endpoint=f'/a/{account_id}', path=f'/companies/{company.id}.json')