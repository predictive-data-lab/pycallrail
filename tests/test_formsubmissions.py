import pytest
import pytest_mock
import requests_mock
import requests

from pycallrail.callrail import CallRail
from pycallrail.objects.form_submissions import FormSubmission
import typing
import logging
import datetime as dt
import typeguard

# Tests that a FormSubmission object can be created with valid arguments. 
def test_create_form_submission_valid_args(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    form_data = {'name': 'John Doe', 'email': 'johndoe@example.com'}
    form_url = 'https://example.com/form'
    landing_page_url = 'https://example.com/landing'
    referrer = 'https://google.com'
    referring_url = 'https://google.com/search?q=example'
    submitted_at = dt.datetime.now()
    first_form = True
    customer_phone_number = '123-456-7890'
    customer_name = 'John Doe'
    formatted_customer_phone_number = '+11234567890'
    formatted_customer_name = 'John D.'
    source = 'Google'
    keywords = 'example'
    campaign = 'Example Campaign'
    medium = 'Organic'

    # Act
    form_submission = FormSubmission(
        api_client=api_client,
        account_id=account_id,
        id='456',
        company_id='789',
        person_id='012',
        form_data=form_data,
        form_url=form_url,
        landing_page_url=landing_page_url,
        referrer=referrer,
        referring_url=referring_url,
        submitted_at=submitted_at,
        first_form=first_form,
        customer_phone_number=customer_phone_number,
        customer_name=customer_name,
        formatted_customer_phone_number=formatted_customer_phone_number,
        formatted_customer_name=formatted_customer_name,
        source=source,
        keywords=keywords,
        campaign=campaign,
        medium=medium
    )

    # Assert
    assert isinstance(form_submission, FormSubmission)
    assert form_submission.api_client == api_client
    assert form_submission.account_id == account_id
    assert form_submission.id == '456'
    assert form_submission.company_id == '789'
    assert form_submission.person_id == '012'
    assert form_submission.form_data == form_data
    assert form_submission.form_url == form_url
    assert form_submission.landing_page_url == landing_page_url
    assert form_submission.referrer == referrer
    assert form_submission.referring_url == referring_url
    assert form_submission.submitted_at == submitted_at
    assert form_submission.first_form == first_form
    assert form_submission.customer_phone_number == customer_phone_number
    assert form_submission.customer_name == customer_name
    assert form_submission.formatted_customer_phone_number == formatted_customer_phone_number
    assert form_submission.formatted_customer_name == formatted_customer_name
    assert form_submission.source == source
    assert form_submission.keywords == keywords
    assert form_submission.campaign == campaign
    assert form_submission.medium == medium

# Tests that a FormSubmission object can be updated with valid arguments. 
def test_update_form_submission_valid_args(mocker: pytest_mock.MockerFixture) -> None:
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    form_submission = FormSubmission(
        api_client=api_client,
        account_id=account_id,
        id='456',
        company_id='789',
        person_id='012',
        form_data={'name': 'John Doe', 'email': 'johndoe@example.com'},
        form_url='https://example.com/form',
        landing_page_url='https://example.com/landing',
        referrer='https://google.com',
        referring_url='https://google.com/search?q=example',
        submitted_at=dt.datetime.now(),
        first_form=True,
        customer_phone_number='123-456-7890',
        customer_name='John Doe',
        formatted_customer_phone_number='+11234567890',
        formatted_customer_name='John D.',
        source='Google',
        keywords='example',
        campaign='Example Campaign',
        medium='Organic'
    )

    api_client._put.return_value = {
        'id': '456',
        'company_id': '789',
        'person_id': '012',
        'form_data': {'name': 'John Doe', 'email': 'johndoe@example.com'},
        'form_url': 'https://example.com/form',
        'landing_page_url': 'https://example.com/landing',
        'referrer': 'https://google.com',
        'referring_url': 'https://google.com/search?q=example',
        'submitted_at': '2021-01-01T00:00:00+00:00',
        'first_form': True
    }
    # Act
    form_submission.update(
        tags=['tag1', 'tag2'],
        note='Example note',
        value=100,
        lead_status='New',
        append_tags=True
    )

    # Assert
    assert form_submission.tags == ['tag1', 'tag2']
    assert form_submission.note == 'Example note'
    assert form_submission.value == 100
    assert form_submission.lead_status == 'New'

# Tests that a FormSubmission object cannot be updated with missing or invalid optional arguments. 
def test_update_form_submission_missing_args(mocker: pytest_mock.MockerFixture):
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    form_submission = FormSubmission(
        api_client=api_client,
        account_id=account_id,
        id='456',
        company_id='789',
        person_id='012',
        form_data={'name': 'John Doe', 'email': 'johndoe@example.com'},
        form_url='https://example.com/form',
        landing_page_url='https://example.com/landing',
        referrer='https://google.com',
        referring_url='https://google.com/search?q=example',
        submitted_at=dt.datetime.now(),
        first_form=True,
        customer_phone_number='123-456-7890',
        customer_name='John Doe',
        formatted_customer_phone_number='+11234567890',
        formatted_customer_name='John D.',
        source='Google',
        keywords='example',
        campaign='Example Campaign',
        medium='Organic'
    )

    # Act and Assert
    with pytest.raises(TypeError):
        form_submission.update(
            tags=['tag1', 'tag2'],
            note='Example note',
            value=100,
            lead_status='New',
            invalid_arg=True
        )

# Tests that a FormSubmission object is not updated if no changes are made. 
def test_update_form_submission_no_changes(mocker: pytest_mock.MockerFixture):
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    form_submission = FormSubmission(
        api_client=api_client,
        account_id=account_id,
        id='456',
        company_id='789',
        person_id='012',
        form_data={'name': 'John Doe', 'email': 'johndoe@example.com'},
        form_url='https://example.com/form',
        landing_page_url='https://example.com/landing',
        referrer='https://google.com',
        referring_url='https://google.com/search?q=example',
        submitted_at=dt.datetime.now(),
        first_form=True,
        customer_phone_number='123-456-7890',
        customer_name='John Doe',
        formatted_customer_phone_number='+11234567890',
        formatted_customer_name='John D.',
        source='Google',
        keywords='example',
        campaign='Example Campaign',
        medium='Organic'
    )

    api_client._put.return_value = {
        'id': '456',
        'company_id': '789',
        'person_id': '012',
        'form_data': {'name': 'John Doe', 'email': 'johndoe@example.com'},
        'form_url': 'https://example.com/form',
        'landing_page_url': 'https://example.com/landing',
        'referrer': 'https://google.com',
        'referring_url': 'https://google.com/search?q=example',
        'submitted_at': '2021-01-01T00:00:00+00:00',
        'first_form': True
    }

    # Act
    form_submission.update()

    # Assert
    assert hasattr(form_submission, 'tags') is False
    assert hasattr(form_submission, 'note') is False
    assert hasattr(form_submission, 'value') is False
    assert hasattr(form_submission, 'lead_status') is False

    # Tests that a FormSubmission object can be deserialized from JSON. 
def test_deserialize_form_submission_from_json(mocker: pytest_mock.MockerFixture):
    # Arrange
    api_client = mocker.Mock(spec=CallRail)
    account_id = '123'
    json_data = {
        "id": "FOR8154748ae6bd4e278a7cddd38a662f4f",
        "company_id": "COM8154748ae6bd4e278a7cddd38a662f4f",
        "person_id": "anonymous",
        "form_data": {
            "name": "Graham Armstrong",
            "email": "graham@example.com",
            "phone": "(999) 999-9999",
            "contact_method": "call",
            "best_time_to_call": "evening"
        },
        "form_url": "http://www.uptowndental.com/appointment",
        "landing_page_url": "http://www.uptowndental.com/appointment?campaign=back_to_school&keywords=pediatric%20dentist&gclid=12345abgdef",
        "referrer": "www.google.com",
        "referring_url": "www.google.com",
        "submitted_at": "2017-11-17T07:46:28.000Z",
        "first_form": False,
        "customer_phone_number": "+19999999999",
        "customer_name": "Graham Armstrong",
        "formatted_customer_phone_number": "999-999-9999",
        "formatted_customer_name": "Graham Armstrong",
        "source": "Google Ads",
        "keywords": "pediatric dentist",
        "campaign": "back_to_school",
        "medium": "CPC",
        "milestones": {
            "first_touch": {
                "event_date": "2017-10-22T19:41:45.183-04:00",
                "ad_position": None,
                "campaign": "back_to_school",
                "device": "desktop",
                "keywords": "pediatric dentist",
                "landing": "http://www.uptowndental.com/appointment?campaign=back_to_school&keywords=pediatric%20dentist&gclid=12345abgdef",
                "landing_page_url_params": {
                        "campaign": "back_to_school",
                        "keywords": "pediatric dentist",
                        "gclid": "12345abgdef"
                },
                "match_type": None,
                "medium": "cpc",
                "referrer": "https://www.google.com/",
                "referrer_url_params": {},
                "session_browser": "Chrome",
                "url_utm_params": {},
                "source": "Google Ads"
            },
            "lead_created": {
                "event_date": "2017-10-22T19:41:45.183-04:00",
                "ad_position": None,
                "campaign": "back_to_school",
                "device": "desktop",
                "keywords": "pediatric dentist",
                "landing": "http://www.uptowndental.com/appointment?campaign=back_to_school&keywords=pediatric%20dentist&gclid=12345abgdef",
                "landing_page_url_params": {
                        "campaign": "back_to_school",
                        "keywords": "pediatric dentist",
                        "gclid": "12345abgdef"
                },
                "match_type": None,
                "medium": "cpc",
                "referrer": "https://www.google.com/",
                "referrer_url_params": {},
                "session_browser": "Chrome",
                "url_utm_params": {},
                "source": "Google Ads"
            },
            "qualified": {
                "event_date": "2017-10-22T19:41:45.183-04:00",
                "ad_position": None,
                "campaign": "back_to_school",
                "device": "desktop",
                "keywords": "pediatric dentist",
                "landing": "http://www.uptowndental.com/appointment?campaign=back_to_school&keywords=pediatric%20dentist&gclid=12345abgdef",
                "landing_page_url_params": {
                        "campaign": "back_to_school",
                        "keywords": "pediatric dentist",
                        "gclid": "12345abgdef"
                },
                "match_type": None,
                "medium": "cpc",
                "referrer": "https://www.google.com/",
                "referrer_url_params": {},
                "session_browser": "Chrome",
                "url_utm_params": {},
                "source": "Google Ads"
            },
            "last_touch": {
                "event_date": "2017-11-17T07:46:28.000-04:00",
                "ad_position": None,
                "campaign": None,
                "device": "desktop",
                "keywords": None,
                "landing": "https://www.example.com/",
                "landing_page_url_params": {},
                "match_type": None,
                "medium": "organic",
                "referrer": "https://www.google.com/",
                "referrer_url_params": {},
                "session_browser": "Chrome",
                "url_utm_params": {},
                "source": "Google Organic"
            }
        }
    }

    # Act
    form_submission: FormSubmission = FormSubmission.from_json(
        api_client=api_client,
        account_id=account_id,
        json_data=json_data
    )

    # Assert
    assert isinstance(form_submission, FormSubmission)
    assert form_submission.api_client == api_client
    assert form_submission.account_id == account_id
    assert form_submission.id == json_data['id']
    assert form_submission.company_id == json_data['company_id']
    assert form_submission.person_id == json_data['person_id']
    assert form_submission.form_data == json_data['form_data']
    assert form_submission.form_url == json_data['form_url']
    assert form_submission.landing_page_url == json_data['landing_page_url']
    assert form_submission.referrer == json_data['referrer']
    assert form_submission.referring_url == json_data['referring_url']
    assert isinstance(form_submission.submitted_at, dt.datetime)
    assert form_submission.first_form == json_data['first_form']
    assert form_submission.customer_phone_number == json_data['customer_phone_number']
    assert form_submission.customer_name == json_data['customer_name']
    assert form_submission.formatted_customer_phone_number == json_data['formatted_customer_phone_number']
    assert form_submission.formatted_customer_name == json_data['formatted_customer_name']
    assert form_submission.source == json_data['source']
    assert form_submission.keywords == json_data['keywords']
    assert form_submission.campaign == json_data['campaign']
    assert form_submission.medium == json_data['medium']
    assert form_submission.milestones == json_data['milestones']