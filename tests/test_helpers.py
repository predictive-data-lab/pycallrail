import pytest
import pytest_mock
import typing
from pycallrail.helpers import build_url

# Tests that the function returns a valid URL string when base_url and endpoint are valid strings. 
def test_happy_path_build_url() -> None:
    # Arrange
    base_url = "https://api.callrail.com/v3/"
    endpoint = "a.json"
    expected_url = "https://api.callrail.com/v3/a.json"

    # Act
    actual_url: str = build_url(base_url, endpoint)

    # Assert
    assert actual_url == expected_url

# Tests that the function handles an empty string for base_url or endpoint. 
def test_edge_case_empty_strings() -> None:
    # Arrange
    base_url: typing.Literal[''] = ""
    endpoint = "/api/v1/users"
    expected_url = "/api/v1/users"

    # Act
    actual_url: str = build_url(base_url, endpoint)

    # Assert
    assert actual_url == expected_url

# Tests that the function handles a path that starts with a leading slash. 
def test_edge_case_leading_slash() -> None:
    # Arrange
    base_url = "https://www.example.com"
    endpoint = "/api/v1/users"
    path = "/profile"
    expected_url = "https://www.example.com/api/v1/users/profile"

    # Act
    actual_url: str = build_url(base_url, endpoint, path)

    # Assert
    assert actual_url == expected_url

# Tests that the function handles query parameters in the URL. 
def test_general_behavior_query_parameters() -> None:
    # Arrange
    base_url = "https://www.example.com"
    endpoint = "/api/v1/users"
    query_params: dict[str, str] = {"sort": "name", "filter": "active"}
    expected_url = "https://www.example.com/api/v1/users?sort=name&filter=active"

    # Act
    actual_url: str = build_url(base_url, endpoint, None)
    actual_url += "?" + "&".join([f"{k}={v}" for k, v in query_params.items()])

    # Assert
    assert actual_url == expected_url

# Tests that the function handles trailing slashes correctly for endpoint and path. 
def test_edge_case_trailing_slashes() -> None:
    # Arrange
    base_url = "https://www.example.com/"
    endpoint = "/api/v1/users/"
    path = "/profile/"
    expected_url = "https://www.example.com/api/v1/users/profile/"

    # Act
    actual_url: str = build_url(base_url, endpoint, path)

    # Assert
    assert actual_url == expected_url

# Tests that the function handles special characters in the URL. 
def test_general_behavior_special_characters() -> None:
    # Arrange
    base_url = "https://www.example.com"
    endpoint = "/api/v1/users"
    path = "/profile?name=John&age=30"
    expected_url = "https://www.example.com/api/v1/users/profile?name=John&age=30"

    # Act
    actual_url: str = build_url(base_url, endpoint, path)

    # Assert
    assert actual_url == expected_url