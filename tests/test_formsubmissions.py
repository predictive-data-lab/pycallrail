import pytest
from unittest.mock import patch, MagicMock
from pytest_mock import MockerFixture
from requests_mock.mocker import Mocker
from pycallrail.callrail import CallRail
from pycallrail.api.accounts import Account
from pycallrail.api.form_submissions import FormSubmission
from requests import Response
from typing import Union, Generator
import requests_mock
import requests
import datetime as dt


# Tests that a FormSubmission object can be created with valid data. 
def test_creating_valid_FormSubmission_object():
    account_data: dict[str, str] = {
        'id': '123',
        'name': 'Test Account'
    }
    form_data = {
        'id': '456',
        'company_id': '789',
        'person_id': '101112',
        'form_data': {'field1': 'value1', 'field2': 'value2'},
        'form_url': 'https://example.com/form',
        'landing_page_url': 'https://example.com/landing',
        'referrer': 'https://example.com/referrer',
        'referring_url': 'https://example.com/referring',
        'submitted_at': '2022-01-01T00:00:00.000000',
        'first_form': True,
        'customer_phone_number': '123-456-7890',
        'customer_name': 'John Doe',
        'formatted_customer_phone_number': '+11234567890',
        'formatted_customer_name': 'John D.',
        'source': 'Google Ads',
        'keywords': 'example keywords',
        'campaign': 'example campaign',
        'medium': 'example medium',
        'lead_status': 'New',
        'value': 100.0,
        'note': 'example note',
        'tags': ['tag1', 'tag2'],
        'utm_source': 'example source',
        'utm_medium': 'example medium',
        'utm_campaign': 'example campaign',
        'form_name': 'example form',
        'timeline_url': 'https://example.com/timeline'
    }
    account = Account(account_data, CallRail(api_key='api_key'))
    form_submission = FormSubmission(account, form_data)
    assert form_submission.id == form_data['id']
    assert form_submission.company_id == form_data['company_id']
    assert form_submission.person_id == form_data['person_id']
    assert form_submission.form_data == form_data['form_data']
    assert form_submission.form_url == form_data['form_url']
    assert form_submission.landing_page_url == form_data['landing_page_url']
    assert form_submission.referrer == form_data['referrer']
    assert form_submission.referring_url == form_data['referring_url']
    assert form_submission.submitted_at == dt.datetime.fromisoformat(form_data['submitted_at'])
    assert form_submission.first_form == form_data['first_form']
    assert form_submission.customer_phone_number == form_data['customer_phone_number']
    assert form_submission.customer_name == form_data['customer_name']
    assert form_submission.formatted_customer_phone_number == form_data['formatted_customer_phone_number']
    assert form_submission.formatted_customer_name == form_data['formatted_customer_name']
    assert form_submission.source == form_data['source']
    assert form_submission.keywords == form_data['keywords']
    assert form_submission.campaign == form_data['campaign']
    assert form_submission.medium == form_data['medium']
    assert form_submission.lead_status == form_data['lead_status']
    assert form_submission.value == form_data['value']
    assert form_submission.note == form_data['note']
    assert form_submission.tags == form_data['tags']
    assert form_submission.utm_source == form_data['utm_source']
    assert form_submission.utm_medium == form_data['utm_medium']
    assert form_submission.utm_campaign == form_data['utm_campaign']
    assert form_submission.form_name == form_data['form_name']
    assert form_submission.timeline_url == form_data['timeline_url']

# Tests that a FormSubmission object can be updated with valid data. 
def test_updating_valid_FormSubmission_object():
    account_data: dict[str, str] = {
        'id': '123',
        'name': 'Test Account'
    }
    initial_form_data = {
        'id': '456',
        'company_id': '789',
        'person_id': '101112',
        'form_data': {'field1': 'value1', 'field2': 'value2'},
        'form_url': 'https://example.com/form',
        'landing_page_url': 'https://example.com/landing',
        'referrer': 'https://example.com/referrer',
        'referring_url': 'https://example.com/referring',
        'submitted_at': '2022-01-01T00:00:00.000000',
        'first_form': True,
        'customer_phone_number': '123-456-7890',
        'customer_name': 'John Doe',
        'formatted_customer_phone_number': '+11234567890',
        'formatted_customer_name': 'John D.',
        'source': 'Google Ads',
        'keywords': 'example keywords',
        'campaign': 'example campaign',
        'medium': 'example medium',
        'lead_status': 'New',
        'value': 100.0,
        'note': 'example note',
        'tags': ['tag1', 'tag2'],
        'utm_source': 'example source',
        'utm_medium': 'example medium',
        'utm_campaign': 'example campaign',
        'form_name': 'example form',
        'timeline_url': 'https://example.com/timeline'
    }
    updated_form_data = {
        'id': initial_form_data['id'],
        'company_id': initial_form_data['company_id'],
        'person_id': initial_form_data['person_id'],
        'form_data': {'field1': 'updated value1', 'field2': 'updated value2'},
        'form_url': initial_form_data['form_url'],
        'landing_page_url': initial_form_data['landing_page_url'],
        'referrer': initial_form_data['referrer'],
        'referring_url': initial_form_data['referring_url'],
        'submitted_at': initial_form_data['submitted_at'],
        'first_form': initial_form_data['first_form'],
        'customer_phone_number': initial_form_data['customer_phone_number'],
        'customer_name': initial_form_data['customer_name'],
        'formatted_customer_phone_number': initial_form_data['formatted_customer_phone_number'],
        'formatted_customer_name': initial_form_data['formatted_customer_name'],
        'source': initial_form_data['source'],
        'keywords': initial_form_data['keywords'],
        'campaign': initial_form_data['campaign'],
        'medium': initial_form_data['medium'],
        'lead_status': 'Updated',
        'value': 200.0,
        'note': 'updated note',
        'tags': ['tag1', 'tag3'],
        'utm_source': initial_form_data['utm_source'],
        'utm_medium': initial_form_data['utm_medium'],
        'utm_campaign': initial_form_data['utm_campaign'],
        'form_name': initial_form_data['form_name'],
        'timeline_url': initial_form_data['timeline_url']
    }
    account = Account(account_data, CallRail(api_key='api_key'))
    form_submission = FormSubmission(account, initial_form_data)
    form_submission.update(updated_form_data)
    assert form_submission.id == updated_form_data['id']
    assert form_submission.company_id == updated_form_data['company_id']
    assert form_submission.person_id == updated_form_data['person_id']
    assert form_submission.form_data == updated_form_data['form_data']
    assert form_submission.form_url == updated_form_data['form_url']
    assert form_submission.landing_page_url == updated_form_data['landing_page_url']
    assert form_submission.referrer == updated_form_data['referrer']
    assert form_submission.referring_url == updated_form_data['referring_url']
    assert form_submission.submitted_at == dt.datetime.fromisoformat(updated_form_data['submitted_at'])
    assert form_submission.first_form == updated_form_data['first_form']
    assert form_submission.customer_phone_number == updated_form_data['customer_phone_number']
    assert form_submission.customer_name == updated_form_data['customer_name']
    assert form_submission.formatted_customer_phone_number == updated_form_data['formatted_customer_phone_number']
    assert form_submission.formatted_customer_name == updated_form_data['formatted_customer_name']
    assert form_submission.source == updated_form_data['source']
    assert form_submission.keywords == updated_form_data['keywords']
    assert form_submission.campaign == updated_form_data['campaign']
    assert form_submission.medium == updated_form_data['medium']
    assert form_submission.lead_status == updated_form_data['lead_status']
    assert form_submission.value == updated_form_data['value']
    assert form_submission.note == updated_form_data['note']
    assert form_submission.tags == updated_form_data['tags']
    assert form_submission.utm_source == updated_form_data['utm_source']
    assert form_submission.utm_medium == updated_form_data['utm_medium']
    assert form_submission.utm_campaign == updated_form_data['utm_campaign']
    assert form_submission.form_name == updated_form_data['form_name']
    assert form_submission.timeline_url == updated_form_data['timeline_url']

# Tests that a FormSubmission object cannot be created with missing or invalid data. 
def test_creating_FormSubmission_object_with_missing_or_invalid_data():
    account_data: dict[str, str] = {
        'id': '123',
        'name': 'Test Account'
    }
    invalid_form_data = {
        'id': '456',
        'company_id': '789',
        'person_id': '101112',
        'form_data': {'field1': 'value1', 'field2': 'value2'},
        'form_url': 'https://example.com/form',
        'landing_page_url': 'https://example.com/landing',
        'referrer': 'https://example.com/referrer',
        'referring_url': 'https://example.com/referring',
        'submitted_at': 'invalid date',
        'first_form': True,
        'customer_phone_number': '123-456-7890',
        'customer_name': 'John Doe',
        'formatted_customer_phone_number': '+11234567890',
        'formatted_customer_name': 'John D.',
        'source': 'Google Ads',
        'keywords': 'example keywords',
        'campaign': 'example campaign',
        'medium': 'example medium',
        'lead_status': 'New',
        'value': 100.0,
        'note': 'example note',
        'tags': ['tag1', 'tag2'],
        'utm_source': 'example source',
        'utm_medium': 'example medium',
        'utm_campaign': 'example campaign',
        'form_name': 'example form',
        'timeline_url': 'https://example.com/timeline'
    }
    account = Account(account_data, CallRail(api_key='api_key'))
    with pytest.raises(Exception):
        FormSubmission(account, invalid_form_data)

# Tests that a FormSubmission object cannot be updated with missing or invalid data. 
def test_updating_FormSubmission_object_with_missing_or_invalid_data():
    account_data: dict[str, str] = {
        'id': '123',
        'name': 'Test Account'
    }
    initial_form_data = {
        'id': '456',
        'company_id': '789',
        'person_id': '101112',
        'form_data': {'field1': 'value1', 'field2': 'value2'},
        'form_url': 'https://example.com/form',
        'landing_page_url': 'https://example.com/landing',
        'referrer': 'https://example.com/referrer',
        'referring_url': 'https://example.com/referring',
        'submitted_at': '2022-01-01T00:00:00.000000',
        'first_form': True,
        'customer_phone_number': '123-456-7890',
        'customer_name': 'John Doe',
        'formatted_customer_phone_number': '+11234567890',
        'formatted_customer_name': 'John D.',
        'source': 'Google Ads',
        'keywords': 'example keywords',
        'campaign': 'example campaign',
        'medium': 'example medium',
        'lead_status': 'New',
        'value': 100.0,
        'note': 'example note',
        'tags': ['tag1', 'tag2'],
        'utm_source': 'example source',
        'utm_medium': 'example medium',
        'utm_campaign': 'example campaign',
        'form_name': 'example form',
        'timeline_url': 'https://example.com/timeline'
    }
    invalid_update_data = {
        'id': initial_form_data['id'],
        'company_id': initial_form_data['company_id'],
        'person_id': initial_form_data['person_id'],
        'form_data': {'field1': 'updated value1', 'field2': 'updated value2'},
        'form_url': initial_form_data['form_url'],
        'landing_page_url': initial_form_data['landing_page_url'],
        'referrer': initial_form_data['referrer'],
        'referring_url': initial_form_data['referring_url'],
        'submitted_at': 'invalid date',
        'first_form': initial_form_data['first_form'],
        'customer_phone_number': initial_form_data['customer_phone_number'],
        'customer_name': initial_form_data['customer_name'],
        'formatted_customer_phone_number': initial_form_data['formatted_customer_phone_number'],
        'formatted_customer_name': initial_form_data['formatted_customer_name'],
        'source': initial_form_data['source'],
        'keywords': initial_form_data['keywords'],
        'campaign': initial_form_data['campaign'],
        'medium': initial_form_data['medium'],
        'lead_status': 'Updated',
        'value': 200.0,
        'note': 'updated note',
        'tags': ['tag1', 'tag3'],
        'utm_source': initial_form_data['utm_source'],
        'utm_medium': initial_form_data['utm_medium'],
        'utm_campaign': initial_form_data['utm_campaign'],
        'form_name': initial_form_data['form_name'],
        'timeline_url': initial_form_data['timeline_url']
    }
    account = Account(account_data, CallRail(api_key='api_key'))
    form_submission = FormSubmission(account, initial_form_data)
    with pytest.raises(ValueError):
        form_submission.update(invalid_update_data)

