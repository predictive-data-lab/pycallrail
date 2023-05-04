import pytest
import pytest_mock
import requests_mock
import requests

from pycallrail.callrail import CallRail
from pycallrail.objects.tags import Tag
import typing
import logging
import datetime as dt
import typeguard

# Tests creating a Tag object with valid input parameters. 
def test_create_tag_valid_input(mocker: pytest_mock.MockerFixture):
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    
    account_id = "123ABC"

    json_data: typing.Dict[str, typing.Any] = {
        "id": 1234569,
        "name": "Existing Customer",
        "tag_level": "company",
        "color": "gray1",
        "background_color": "gray1",
        "company_id": "COM8154748ae6bd4e278a7cddd38a662f4f",
        "status": "enabled",
        "created_at": "2014-06-06T12:11:02.964-04:00"
    }

    api_client._post.return_value = json_data

    # Act
    tag = Tag.from_json(api_client, account_id, json_data)

    # Assert
    assert tag.id == json_data["id"]
    assert tag.name == json_data["name"]
    assert tag.tag_level == json_data["tag_level"]
    assert tag.color == json_data["color"]
    assert tag.background_color == json_data["background_color"]
    assert tag.company_id == json_data["company_id"]
    assert tag.status ==   json_data["status"]
    assert tag.created_at == json_data["created_at"]
    assert isinstance(tag.created_at, dt.datetime)

# Tests updating a Tag object with valid input parameters. 
def test_update_tag_valid_input(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)

    account_id = '123ABC'
    id = 1234569
    name = 'Existing Customer - Old Name'
    tag_level = 'company'
    color = 'gray2'
    background_color = 'gray1'
    company_id = 'COM8154748ae6bd4e278a7cddd38a662f4f'
    status = 'enabled'
    created_at: dt.datetime = dt.datetime.now()

    update_data: typing.Dict[str, str] = {
           "name": "Existing Customer",
           "color": "gray1"
    }

    json_data: typing.Dict[str, str] = {
        "id": "1234569",
        "name": "Existing Customer",
        "tag_level": "company",
        "color": "gray1",
        "background_color": "gray1",
        "company_id": "COM8154748ae6bd4e278a7cddd38a662f4f",
        "status": "enabled",
        "created_at": "2014-06-06T12:11:02.964-04:00"
    }

    api_client._put.return_value = json_data

    tag = Tag(api_client, account_id, id, name, tag_level, color, background_color, company_id, status, created_at)

    # Act
    tag.update(name=update_data["name"], color=update_data["color"])

    # Assert
    assert tag.name == update_data["name"]
    assert tag.color == update_data["color"]
    
# Tests creating a Tag object with invalid input parameters. 
def test_create_tag_invalid_input(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    id = 1
    name = None
    tag_level = 'company'
    color = '#FFFFFF'
    background_color = '#000000'
    company_id = '456'
    status = 'active'
    created_at: dt.datetime = dt.datetime.now()

    json_data: typing.Dict[str, typing.Any] = {
        'id': id,
        'name': name,
        'tag_level': tag_level,
        'color': color,
        'background_color': background_color,
        'company_id': company_id,
        'status': status,
        'created_at': created_at.isoformat()
    }

    api_client._post.return_value = json_data

    # Act and Assert
    with pytest.raises(typeguard.TypeCheckError):
        Tag.from_json(api_client, account_id, json_data)

# Tests deleting a Tag object. 
def test_delete_tag(mocker: pytest_mock.MockerFixture):
    # Arrange
    api_client = mocker.Mock()
    account_id = '123'
    id = 1
    name = 'Test Tag'
    tag_level = 'company'
    color = '#FFFFFF'
    background_color = '#000000'
    company_id = '456'
    status = 'active'
    created_at: dt.datetime = dt.datetime.now()

    tag = Tag(api_client, account_id, id, name, tag_level, color, background_color, company_id, status, created_at)

    # Act
    tag.delete()

    # Assert
    api_client._delete.assert_called_once_with(endpoint=f'a/{account_id}', path=f'tags/{id}.json')

# Tests deleting a non-existent Tag object. 
def test_delete_nonexistent_tag(mocker: pytest_mock.MockerFixture):
    # Arrange
    api_client = mocker.Mock()
    account_id = '123'
    id = 1
    name = 'Test Tag'
    tag_level = 'company'
    color = '#FFFFFF'
    background_color = '#000000'
    company_id = '456'
    status = 'active'
    created_at = dt.datetime.now()

    tag = Tag(api_client, account_id, id, name, tag_level, color, background_color, company_id, status, created_at)

    api_client._delete.side_effect = Exception('Tag not found')

    # Act and Assert
    with pytest.raises(Exception):
        tag.delete()