import pytest
from unittest.mock import patch, MagicMock
from pytest_mock import MockerFixture
from requests_mock.mocker import Mocker
from pycallrail.callrail import CallRail
from pycallrail.api.accounts import Account
from pycallrail.api.call import Call, CallType
from pycallrail.api.tag import Tag
from pycallrail.api.companies import Company
from requests import Response
from typing import Union, Generator, Any
import requests_mock
import requests
import datetime as dt

# Tests that a Tag object can be created with valid data. 
def test_create_tag_with_valid_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    data: dict[str, str] = {
        "id": "123",
        "name": "Test Tag",
        "tag_level": "1",
        "color": "#FFFFFF",
        "background_color": "#000000",
        "company_id": "456",
        "status": "active",
        "created_at": "2022-01-01T00:00:00.000"
    }
    
    # Act
    tag = Tag(data, parent)
    
    # Assert
    assert tag.id == "123"
    assert tag.name == "Test Tag"
    assert tag.tag_level == "1"
    assert tag.color == "#FFFFFF"
    assert tag.background_color == "#000000"
    assert tag.company_id == "456"
    assert tag.status == "active"
    assert tag.created_at == dt.datetime(2022, 1, 1)

# Tests that a Tag object can be updated with valid data. 
def test_update_tag_with_valid_data(mocker: MockerFixture) -> None:
    # Arrange
    parent = mocker.Mock(spec=Account)
    data: dict[str, str] = {
        "id": "123",
        "name": "Test Tag",
        "tag_level": "1",
        "color": "#FFFFFF",
        "background_color": "#000000",
        "company_id": "456",
        "status": "active",
        "created_at": "2022-01-01T00:00:00.000"
    }
    tag = Tag(data, parent)
    update_data: dict[str, str] = {
        "name": "Updated Tag",
        "color": "#000000"
    }
    

    # Act
    tag.update(
        update_data=update_data,
        keys=update_data.keys(),
        all=False
    )
    
    

    # Assert
    assert tag.name == "Updated Tag"
    assert tag.color == "#000000"

# Tests that a Tag object cannot be created with missing data. 
def test_create_tag_with_missing_data(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    data: dict[str, str] = {
        "id": "123",
        "name": "Test Tag",
        "tag_level": "1",
        "color": "#FFFFFF",
        "background_color": "#000000",
        "company_id": "456"
    }
    
    # Act/Assert
    with pytest.raises(AttributeError):
        tag = Tag(data, parent)

# Tests that a Tag object cannot be created with invalid data types. 
def test_create_tag_with_invalid_data_types(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    data = {
        "id": False,
        "name": "Test Tag",
        "tag_level": "1",
        "color": "#FFFFFF",
        "background_color": "#000000",
        "company_id": "456",
        "status": "active",
        "created_at": "2022-01-01T00:00:00.000Z"
    }
    
    # Act/Assert
    with pytest.raises(TypeError):
        tag = Tag(data, parent)

# Tests that a Tag object can be successfully deleted. 
def test_delete_existing_tag(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock(spec=Account({"id": "456"}, parent=mocker.Mock(spec=CallRail)))
    data: dict[str, str] = {
        "id": "123",
        "name": "Test Tag",
        "tag_level": "1",
        "color": "#FFFFFF",
        "background_color": "#000000",
        "company_id": "456",
        "status": "active",
        "created_at": "2022-01-01T00:00:00.000"
    }
    tag = Tag(data, parent)
    
    # Act
    tag.delete()
    
    # Assert
    parent.parent._delete.assert_called_once_with(endpoint='a', path='/456/tags/123.json')

# Tests that a Tag object cannot be updated with invalid data types. 
def test_update_tag_with_invalid_data_types(mocker: MockerFixture):
    # Arrange
    parent = mocker.Mock()
    data: dict[str, str] = {
        "id": "123",
        "name": "Test Tag",
        "tag_level": "1",
        "color": "#FFFFFF",
        "background_color": "#000000",
        "company_id": "456",
        "status": "active",
        "created_at": "2022-01-01T00:00:00.000"
    }
    tag = Tag(data, parent)
    update_data: dict[str, Any] = {
        "name": 123,
        "color": "#000000"
    }
    
    # Act/Assert
    with pytest.raises(TypeError):
        tag.update(update_data)