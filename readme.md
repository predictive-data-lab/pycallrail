# CallRail API for Python

[![Tests](https://github.com/kharigardner/pycallrail/actions/workflows/testing.yml/badge.svg?branch=main)](https://github.com/kharigardner/pycallrail/actions/workflows/testing.yml) 
## Overview

I created this library to make it easier to integrate the CallRail API into Python applications. It is a wrapper around the CallRail API, which is documented [here](https://apidocs.callrail.com/).

## Installation

To install the library, run:

```bash
pip install pycallrail
```

## Usage

To use the library, you must first create a `CallRail` object. This object is used to make API calls. You can create a `CallRail` object by passing in your CallRail API key:

```python
from pycallrail.callrail import CallRail

call_rail_api = CallRail(api_key = '<your api key>')
```

A majority of the functionality resides in the usage of the 'Account' class. This class is used to make calls to the CallRail API. The `Account` class can be created through the list_accounts method and get_account method of the `CallRail` object. The `list_accounts` method returns a list of `Account` objects. The `get_account` method returns a single `Account` object.

```python
# Get a list of accounts
accounts = call_rail_api.list_accounts() # kwargs for filtering, searching, fields, supported by the endpoint

main_account = accounts[0]

# Get a single account
account = call_rail_api.get_account(account_id = '123456789abcdefg') # kwargs for filtering, searching, fields, supported by the endpoint
```

### Examples

#### Get a list of calls

```python
calls = main_account.list_calls(
    company_id = '123456789abcdefg', # optional
    tracker_id = '123456789abcdefg',
    sorting = {
        sort = 'created_at',
        order = 'desc'
    } # optional
)

for call in calls:
    print(call.customer_name)
```

#### Send a text message

```python
# get text threads
text_threads = main_account.list_text_message_threads(
    company_id = 'oooe0000eee000', # optional
    filtering = {
        'start_date': '2019-01-01',
        'end_date': '2019-01-31'
    }, # optional
    searching = {
        'search': 'John Doe'
    }, # optional
    fields = {
        'fields': 'id,company_id,phone_number,created_at,updated_at'
    } # optional
)

# send a message in a thread
text_thread = text_threads[0]
text_thread.send_text_message(
    {
        'company_id': 'oooe0000eee000',
        'tracking_number': "5555555555",
        'customer_phone_number': "55555533333",
        'content': 'Hello, this is a test message.'
    }
)