import asyncio
import ujson
import logging
import os
import random
import string
import threading
import time
from dataclasses import dataclass
from typing import Optional, Iterable, AsyncIterable,Generator, AsyncGenerator, ClassVar, Any, List
from urllib.parse import urljoin, urlencode

import aiohttp
import requests
import enum

from api.accounts import *
from api.call import *

from exceptions import BaseCallRailException

BASE_URL = "https://api.callrail.com/v3/"

ERROR_CODES = {
    200: "OK - The request was succeeded.",
    201: "Created - The request was succeeded and a resource was created.",
    204: "No Content - The request was succeeded but there is no content to return.",
    400: "Bad Request - The request was malformed or missing a required parameter.",
    401: "Unauthorized - The API key is invalid.",
    403: "Forbidden - The API key does not have permission to access the requested resource.",
    404: "Not Found - The requested resource could not be found.",
    405: "Method Not Allowed - The requested method is not supported for the specified resource.",
    406: "Not Acceptable - The requested resource is only capable of generating content not acceptable according to the Accept headers sent in the request.",
    422: "Unprocessable Entity - The request was well-formed but was unable to be followed due to semantic errors.",
    429: "Too Many Requests - The API key has exceeded the rate limit.",
    500: "Internal Server Error - We had a problem with our server. Try again later.",
    503: "Service Unavailable - We're temporarily offline for maintenance. Please try again later."
}

class PaginationType(enum.Enum):
    """
    The type of pagination to use.
    """
    RELATIVE = "relative"
    OFFSET = "offset"

class CallRail():
    logger = logging.getLogger(__name__)
    
    def __init__(
            self,
            api_key: str,
            logging_level: int = logging.INFO,
            request_delay: Optional[float or int] = None,
            proxy: Optional[str] = None,
            **kwargs
    ):
        """
        
        The main class for the CallRail API. Allows for prgrammatic access to the CallRail API.
        
        ### Parameters:
        - 'api_key': The API key for the CallRail account.
        - 'logging_level': The logging level. Defaults to logging.INFO.
        - 'request_delay': The delay between requests. Defaults to None.
        - 'proxy': The proxy to use for requests. Defaults to None.
        - 'kwargs': Additional keyword arguments.
        """
        self.logger.setLevel(logging_level)
        self.api_key = api_key
        self.request_delay = request_delay
        self.proxy = proxy
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.auth_header = {
            'Authorization': f'Token token={self.api_key}'
        }

        self.base_relative_pagination_params = {
            'relative_pagination': 'true'
        }

    def _relative_paginator(
            self,
            response: requests.Response,
            response_data_key: str = None
    ) -> Iterable | AsyncIterable | Generator | AsyncGenerator:
        """
        Base relative pagination function for the CallRail API.
        """
        pagination_list = []
        while True:
            try:
                pagination_list.extend(response.json()[response_data_key])
            except KeyError:
                break
            if "next_page" not in response.json() \
                or "has_next_page" not in response.json() \
                      or response.json()["has_next_page"] is False:
                break
            try:
                response = requests.get(
                    response.json()["next_page"],
                    headers=self.auth_header,
                    params=self.base_relative_pagination_params)
                response.raise_for_status()
            except requests.HTTPError as e:
                raise BaseCallRailException(
                    message=f"BASE ERROR {e.errno}",
                    status_code=response.status_code,
                    response=response.json(),
                    headers=response.headers
                ) from e
            except Exception as e:
                raise e
        return pagination_list
    
    def _offset_paginator(
            self,
            response: requests.Response,
            response_data_key: str = None
    ) -> Iterable | AsyncIterable | Generator | AsyncGenerator:
        """
        Base offset pagination function for the CallRail API.
        """
        pagination_list = []
        current_page = response.json()['page']
        total_pages = response.json()['total_pages']

        while True:
            try:
                pagination_list.extend(response.json()[response_data_key])
            except KeyError:
                break
            if current_page == total_pages:
                break
            try:
                response = requests.get(
                    response.json()["next_page"],
                    headers=self.auth_header
                )
                response.raise_for_status()
            except requests.HTTPError as e:
                raise BaseCallRailException(
                    message=f"BASE ERROR {e.errno}",
                    status_code=response.status_code,
                    response=response.json(),
                    headers=response.headers
                ) from e
            except Exception as e:
                raise e
            current_page = response.json()['page']
        return pagination_list
    
    def _get(
            self,
            endpoint: str,
            path: Optional[str] = None,
            params: Optional[dict] = None,
            response_data_key: Optional[str] = None,
            pagination_type: Optional[PaginationType] = PaginationType.OFFSET
    ) -> Iterable[dict] | dict | None:

        """
        Base GET request function for the CallRail API.
        """
        if self.request_delay:
            time.sleep(self.request_delay)
        url = urljoin(BASE_URL, endpoint)
        print(url)
        if path:
            url = f'{url}{path}'
        if params:
            first_response = requests.get(
                url,
                headers=self.auth_header,
                params=params
            )
        else:
            first_response = requests.get(
                url,
                headers=self.auth_header
            )
        first_response.raise_for_status()

        # check if pagination is needed
        if "page" not in first_response.json() \
            or "next_page" not in first_response.json():
            try:
                return first_response.json()[response_data_key]
            except KeyError:
                return first_response.json()

        if pagination_type == PaginationType.RELATIVE:
            return self._relative_paginator(
                response=first_response,
                response_data_key=response_data_key
            )
        elif pagination_type == PaginationType.OFFSET:
            return self._offset_paginator(
                response=first_response,
                response_data_key=response_data_key
            )
        
    def _post(
            self,
            endpoint: str,
            path: Optional[str] = None,
            data: Optional[dict] = None,
            response_data_key: Optional[str] = None
    ) -> Iterable[dict] | dict | None:
        """
        Base POST request function for the CallRail API.
        """
        if self.request_delay:
            time.sleep(self.request_delay)
        url = urljoin(BASE_URL, endpoint)
        if path:
            url = urljoin(url, path)
        if data:
            response = requests.post(
                url,
                headers=self.auth_header,
                data=data
            )
        else:
            response = requests.post(
                url,
                headers=self.auth_header
            )
        response.raise_for_status()
        return response.json()
    
    def _put(
            self,
            endpoint: str,
            path: Optional[str] = None,
            data: Optional[dict] = None,
            response_data_key: Optional[str] = None
    ) -> Iterable[dict] | dict | None:
        """
        Base PUT request function for the CallRail API.
        """
        if self.request_delay:
            time.sleep(self.request_delay)
        url = urljoin(BASE_URL, endpoint)
        if path:
            url = urljoin(url, path)
        if data:
            response = requests.put(
                url,
                headers=self.auth_header,
                data=data
            )
        else:
            response = requests.put(
                url,
                headers=self.auth_header
            )
        response.raise_for_status()
        return response.json()
    

    def _delete(
            self,
            endpoint: str,
            path: Optional[str] = None,
            response_data_key: Optional[str] = None
    ) -> None:
        """
        Base DELETE request function for the CallRail API.
        """
        if self.request_delay:
            time.sleep(self.request_delay)
        url = urljoin(BASE_URL, endpoint)
        if path:
            url = urljoin(url, path)
        response = requests.delete(
            url,
            headers=self.auth_header
        )
        response.raise_for_status()
        
    ##############################
    # Accounts
    ##############################


    def list_accounts(
            self,
            **kwargs
    ) -> List[Account]:  # sourcery skip: remove-none-from-default-get
        """
        List all accounts for the authenticated user.
        """
        sorting: dict = kwargs.get('sorting', None)
        filtering: dict = kwargs.get('filtering', None)
        searching: dict = kwargs.get('searching', None)
        fields: dict = kwargs.get('fields', None)

        params = {}

        if sorting:
            params |= sorting
        if filtering:
            params |= filtering
        if searching:
            params |= searching
        if fields:
            params |= fields

        accounts = self._get(
            params=params,
            endpoint = 'a',
            path = '.json',
            response_data_key='accounts',
            pagination_type= PaginationType.OFFSET
        )

        # If the response is a list, return a list of Account objects.
        if isinstance(accounts, list) and len(accounts) > 1:
            return [Account(account, parent=self) for account in accounts]
        elif isinstance(accounts, list) and len(accounts) == 1:
            return Account(accounts[0], parent=self)
        # If the response is a dict, return a single Account object.
        elif isinstance(accounts, dict):
            return Account(accounts, parent=self)
        else:
            return None
        
    def get_account(
            self,
            account_id: str,
            **kwargs
    ) -> Account:
        """
        Get a single account.
        """
        fields: dict = kwargs.get('fields', None)

        params = {}

        if fields:
            params |= fields

        return Account(
                self._get(
                    endpoint = 'a',
                    path = f'/{account_id}.json',
                    response_data_key='account'
                ), 
            parent=self)