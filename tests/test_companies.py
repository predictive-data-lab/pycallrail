import pytest
from unittest.mock import patch, MagicMock
from pytest_mock import MockerFixture
from requests_mock.mocker import Mocker
from pycallrail.callrail import CallRail
from pycallrail.api.accounts import Account
from pycallrail.api.call import Call, CallType
from pycallrail.api.companies import Company
from requests import Response
from typing import Union, Generator
import requests_mock
import requests
import datetime as dt


# Tests that a Company object can be created with valid data. 
def test_create_company_with_valid_data(mocker: MockerFixture):
    # Arrange
    parent_mock = mocker.Mock(spec=Account)
    data = {
        "name": "Test Company",
        "status": "active",
        "time_zone": "America/New_York",
        "dni_active": True,
        "script_url": "https://example.com/script.js",
        "callscore_enabled": True,
        "lead_scoring_enabled": False,
        "swap_exclude_jquery": False,
        "swap_ppc_override": False,
        "swap_landing_override": False,
        "swap_cookie_duration": 30,
        "keyword_spotting_enabled": True,
        "form_capture": True,
        'id': "123",
        'created_at': '2022-01-01T00:00:00',
        'verified_caller_ids': [{"id": "456", "phone_number": "+1234567890"}]
    }

    # Act
    company = Company(data, parent_mock)

    # Assert
    assert company.id == "123"
    assert company.name == "Test Company"
    assert company.status == "active"
    assert company.time_zone == "America/New_York"
    assert company.created_at == dt.datetime(2022, 1, 1, 0, 0)
    assert company.disabled_at is None
    assert company.dni_active is True
    assert company.script_url == "https://example.com/script.js"
    assert company.callscore_enabled is True
    assert company.lead_scoring_enabled is False
    assert company.swap_exclude_jquery is False
    assert company.swap_ppc_override is False
    assert company.swap_landing_override is False
    assert company.swap_cookie_duration == 30
    assert company.callscribe_enabled is None
    assert company.keyword_spotting_enabled is True
    assert company.form_capture is True
    assert company.verified_caller_ids == [{"id": "456", "phone_number": "+1234567890"}]

# Tests that a Company object can be updated with valid data. 
def test_update_company_with_valid_data(mocker: MockerFixture):
    # Arrange
    mock_parent = mocker.Mock(spec=Account)
    mock_parent.parent._put.return_value = {
        "id": "123",
        "name": "Updated Company",
        "status": "inactive",
        "time_zone": "America/Los_Angeles",
        "created_at": "2022-01-01T00:00:00Z",
        "disabled_at": "2022-01-02T00:00:00Z",
        "dni_active": False,
        "script_url": "https://example.com/updated.js",
        "callscore_enabled": True,
        "lead_scoring_enabled": False,
        "swap_exclude_jquery": True,
        "swap_ppc_override": True,
        "swap_landing_override": True,
        "swap_cookie_duration": 30,
        "callscribe_enabled": True,
        "keyword_spotting_enabled": True,
        "form_capture": True,
        "verified_caller_ids": [{"id": 1, "name": "John Doe"}]
    }
    company_data = {
        "id": "123",
        "name": "Test Company",
        "status": "active",
        "time_zone": "America/New_York",
        "created_at": dt.datetime(2022, 1, 1, 0, 0),
        "disabled_at": None,
        "dni_active": True,
        "script_url": "https://example.com/script.js",
        "callscore_enabled": False,
        "lead_scoring_enabled": True,
        "swap_exclude_jquery": None,
        "swap_ppc_override": None,
        "swap_landing_override": None,
        "swap_cookie_duration": None,
        "callscribe_enabled": None,
        "keyword_spotting_enabled": None,
        "form_capture": None,
        "verified_caller_ids": []
    }
    company = Company(company_data, mock_parent)
    update_data = {
        "name": "Updated Company",
        "status": "inactive",
        "time_zone": "America/Los_Angeles",
        "disabled_at": "2022-01-02T00:00:00Z",
        "dni_active": False,
        "script_url": "https://example.com/updated.js",
        "callscore_enabled": True,
        "lead_scoring_enabled": False,
        "swap_exclude_jquery": True,
        "swap_ppc_override": True,
        "swap_landing_override": True,
        "swap_cookie_duration": 30,
        "callscribe_enabled": True,
        "keyword_spotting_enabled": True,
        "form_capture": True,
        "verified_caller_ids": [{"id": 1, "name": "John Doe"}]
    }

    # Act
    company.update(update_data)

    # Assert
    assert company.id == "123"
    assert company.name == "Updated Company"
    assert company.status == "inactive"
    assert company.time_zone == "America/Los_Angeles"
    assert company.created_at == dt.datetime(2022, 1, 1, 0, 0)
    assert company.disabled_at == dt.datetime(2022, 1, 2, 0, 0)
    assert company.dni_active is False
    assert company.script_url == "https://example.com/updated.js"
    assert company.callscore_enabled is True
    assert company.lead_scoring_enabled is False
    assert company.swap_exclude_jquery is True
    assert company.swap_ppc_override is True
    assert company.swap_landing_override is True
    assert company.swap_cookie_duration == 30
    assert company.callscribe_enabled is True
    assert company.keyword_spotting_enabled is True
    assert company.form_capture is True
    assert company.verified_caller_ids == [{"id": 1, "name": "John Doe"}]

# Tests that a Company object cannot be created with missing or invalid data. 
def test_create_company_with_missing_or_invalid_data(mocker: MockerFixture):
    # Arrange
    mock_parent = mocker.Mock(spec=Account)
    company_data: dict = {
        "name": "Test Company",
        "status": "active",
        "time_zone": "America/New_York",
        'created_at': '2022-01-01T00:00:00',
        "dni_active": True,
        "lead_scoring_enabled": True
    }
    invalid_company_data: dict[str, str] = {
        "name": "",
        "status": "invalid",
        "time_zone": "invalid",
        "dni_active": "invalid",
        "lead_scoring_enabled": "invalid"
    }

    # Act & Assert
    with pytest.raises(ValueError):
        Company(None, mock_parent)
    with pytest.raises(Exception):
        Company(invalid_company_data, mock_parent)
    with pytest.raises(Exception):
        Company(company_data, None)
    
# Tests that a Company object cannot be updated with missing or invalid data. 
def test_update_company_with_missing_or_invalid_data(mocker: MockerFixture):
    # Arrange
    mock_parent = mocker.Mock(spec=Account)
    mock_parent.parent._put.return_value = None
    company_data = {
        "id": "123",
        "name": "Test Company",
        "status": "active",
        "time_zone": "America/New_York",
        "created_at": dt.datetime(2022, 1, 1, 0, 0),
        "disabled_at": None,
        "dni_active": True,
        "script_url": "https://example.com/script.js",
        "callscore_enabled": False,
        "lead_scoring_enabled": True,
        "swap_exclude_jquery": None,
        "swap_ppc_override": None,
        "swap_landing_override": None,
        "swap_cookie_duration": None,
        "callscribe_enabled": None,
        "keyword_spotting_enabled": None,
        "form_capture": None,
        "verrified_caller_ids": []
    }
    company = Company(company_data, mock_parent)
    invalid_update_data = {
        "name": "",
        "status": "invalid",
        "time_zone": "invalid",
        "dni_active": "invalid",
        "lead_scoring_enabled": "invalid"
    }

    # Act & Assert
    with pytest.raises(ValueError):
        company.update(None)
    with pytest.raises(Exception):
        company.update(invalid_update_data)
    with pytest.raises(Exception):
        company.update({})
    with pytest.raises(Exception):
        company.update({"id": "456"})

# Tests that an existing Company object can be deleted.  
def test_delete_existing_company(mocker: MockerFixture):
    # Arrange
    mock_parent = mocker.Mock(spec=Account)
    mock_parent.parent._delete.return_value = None
    company_data = {
        "id": "123",
        "name": "Test Company",
        "status": "active",
        "time_zone": "America/New_York",
        "created_at": "2022-01-01T00:00:00Z",
        "disabled_at": None,
        "dni_active": True,
        "script_url": "https://example.com/script.js",
        "callscore_enabled": True,
        "lead_scoring_enabled": True,
        "swap_exclude_jquery": False,
        "swap_ppc_override": False,
        "swap_landing_override": False,
        "swap_cookie_duration": 30,
        "callscribe_enabled": True,
        "keyword_spotting_enabled": True,
        "form_capture": True,
        "verrified_caller_ids": [{"id": "1", "number": "+1234567890"}],
    }
    company = Company(company_data, mock_parent)

    # Act
    company.delete()

    # Assert
    mock_parent.parent._delete.assert_called_once_with(
        endpoint='a',
        path='/123/companies/123.json'
    )