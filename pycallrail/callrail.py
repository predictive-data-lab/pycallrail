from __future__ import with_statement, print_function, absolute_import, annotations
import requests
import typing
import collections
from urllib.parse import urljoin

from pycallrail.objects.accounts import Account
from pycallrail.helpers import build_url

class CallRail(object):
    """Base class for CallRail API access"""

    def __init__(
            self, 
            api_key: str, 
            proxies: typing.Optional[collections.MutableMapping[str, str]] = None, 
            default_pagination_type: typing.Optional[str] = 'relative'
        ) -> None:
        """
        Constructor
        
        :api_key: API Key for the CallRail Account.
        :proxies: Set of proxies to use.
        """
        if api_key is None:
            raise ValueError('API key is required')
        self.BASE_URL: str = 'https://api.callrail.com/v3/'
        self.api_key: str = api_key
        self.proxies: typing.Union[collections.MutableMapping[str, str], None] = proxies
        
        self.session: requests.Session = requests.Session()
        
        if proxies is not None:
            self.session.proxies = typing.cast(collections.MutableMapping[str, str], proxies)

        self.auth_header: collections.Mapping[str, str] = {
            "Authorization": f'Token token="{self.api_key}"'
        }

        self.session.headers.update(self.auth_header)

        if default_pagination_type == 'relative':
            self.default_pagination_param: collections.MutableMapping[str, str] = {
                'relative_pagination': 'true'
            }

    
    def _relative_paginator(
            self,
            response: requests.Response,
            response_data_key: typing.Optional[str] = None
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        Paginate through API responses using relative pagination
        
        :response: Response object
        :response_data_key: Key to use for response data
        """

        result_bag: list[None] = []

        while True:
            try:
                result_bag.extend(response.json()[response_data_key])
            except KeyError:
                break
            if "next_page" not in response.json() \
                or "has_next_page" not in response.json() \
                    or response.json()['has_next_page'] is False:
                break
            try:
                response = self.session.get(
                    url=response.json()['next_page'],
                    params=self.default_pagination_param
                )
                response.raise_for_status()
            except Exception as e:
                raise e
        
        return typing.cast(typing.List[typing.Dict[str, typing.Any]], result_bag)

    def _offset_paginator(
            self,
            response: requests.Response,
            response_data_key: typing.Optional[str] = None
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        Paginate through API responses using offset pagination
        
        :response: Response object
        :response_data_key: Key to use for response data
        """

        result_bag: list[None] = []
        
        current_page: int = response.json()['page']
        total_pages: int = response.json()['total_pages']

        while True:
            try:
                result_bag.extend(response.json()[response_data_key])
            except KeyError:
                break
            if current_page == total_pages:
                break
            try:
                response = self.session.get(
                    url=f'{response.url}',
                    params={'page': current_page + 1},
                    headers=self.auth_header
                )
                response.raise_for_status()
            except Exception as e:
                raise e
            current_page = response.json()['page']

        return typing.cast(typing.List[typing.Dict[str, typing.Any]], result_bag)
    
    def _get(
            self,
            endpoint: str,
            response_data_key: typing.Optional[str] = None,
            path: typing.Optional[str] = None,
            params: typing.Optional[typing.MutableMapping[str, typing.Any]] = None,
            pagination_type: typing.Optional[str] = 'OFFSET'
    ) -> typing.Union[typing.List[typing.Dict[str, typing.Any]], typing.Dict[str, typing.Any], None]:
        """
        Make a GET request to the CallRail API.
        
        :endpoint: API endpoint
        :path: API path
        :params: Query string parameters
        :response_data_key: Key to use for response data
        """
        if path:
            url: str = build_url(
                base_url=self.BASE_URL,
                endpoint=endpoint,
                path=path
            )
        else:
            url = build_url(
                base_url=self.BASE_URL,
                endpoint=endpoint
            )

        if params:
            if pagination_type == 'RELATIVE':
                params.update(self.default_pagination_param)
            first_response: requests.Response = self.session.get(
                url=url,
                params=params
            )
        else:
            if pagination_type == 'RELATIVE':
                first_response: requests.Response = self.session.get( # type: ignore
                    url=url,
                    params=self.default_pagination_param
                )
            else:
                first_response: requests.Response = self.session.get( # type: ignore
                    url=url
                )

        first_response.raise_for_status()

        if pagination_type == 'OFFSET':
            return self._offset_paginator(
                response=first_response,
                response_data_key=response_data_key
            )
        elif pagination_type == 'RELATIVE':
            return self._relative_paginator(
                response=first_response,
                response_data_key=response_data_key
            )
        
        else:
            return first_response.json()
        
    def _post(
            self,
            endpoint: str,
            path: typing.Optional[str] = None,
            data: typing.Optional[typing.MutableMapping[str, typing.Any]] = None,
            response_data_key: typing.Optional[str] = None
    ) -> typing.Union[typing.List[typing.Dict[str, typing.Any]], typing.Dict[str, typing.Any], None]:
        """
        Make a POST request to the CallRail API.
        
        :endpoint: API endpoint
        :path: API path
        :data: JSON data to send
        :response_data_key: Key to use for response data
        """
        if path:
            url: str = build_url(
                base_url=self.BASE_URL,
                endpoint=endpoint,
                path=path
            )
        else:
            url = build_url(
                base_url=self.BASE_URL,
                endpoint=endpoint
            )

        if data:
            first_response: requests.Response = self.session.post(
                url=url,
                json=data
            )
        else:
            first_response: requests.Response = self.session.post( # type: ignore
                url=url
            )
        
        first_response.raise_for_status()
        return first_response.json()[response_data_key] if response_data_key else first_response.json()
    
    def _put(
            self,
            endpoint: str,
            path: typing.Optional[str],
            data: typing.Optional[typing.MutableMapping[str, typing.Any]],
            response_data_key: typing.Optional[str] = None,
            params: typing.Optional[typing.Mapping[str, typing.Any]] = None
    ) -> typing.Union[typing.List[typing.Dict[str, typing.Any]], typing.Dict[str, typing.Any], None]:
        """
        Make a PUT request to the CallRail API.

        :endpoint: API endpoint
        :path: API path
        :data: JSON data to send
        :response_data_key: Key to use for response data
        """
        if path:
            url: str = build_url(
                base_url=self.BASE_URL,
                endpoint=endpoint,
                path=path
            )
        else:
            url = build_url(
                base_url=self.BASE_URL,
                endpoint=endpoint
            )
        
        if data and params:
            response: requests.Response = self.session.put(
                url=url,
                json=data,
                params=params
            )
        elif data:
            response: requests.Response = self.session.put( # type: ignore
                url=url,
                json=data
            )
        elif params:
            response: requests.Response = self.session.put( # type: ignore
                url=url,
                params=params
            )
        else:
            response: requests.Response = self.session.put( # type: ignore
                url=url
            )
            
        response.raise_for_status()

        return response.json()[response_data_key] if response_data_key else response.json()
    
    def _delete(
            self,
            endpoint: str,
            path: typing.Optional[str] = None,
            response_data_key: typing.Optional[str] = None
    ) -> None:
        """
        Make a DELETE request to the CallRail API.

        endpoint: API endpoint
        :path: API path
        :response_data_key: Key to use for response data
        """
        if path:
            url: str = build_url(
                base_url=self.BASE_URL,
                endpoint=endpoint,
                path=path
            )
        else:
            url = build_url(
                base_url=self.BASE_URL,
                endpoint=endpoint
            )
            
        
        response: requests.Response = self.session.delete(
            url=url
        )
        response.raise_for_status()

    #########################
    # Accounts
    #########################

    def list_accounts(
            self,
            **kwargs
    ) -> typing.List[Account]:
        """
        List accounts for the authenticated user.
        """

        sorting: typing.Optional[collections.MutableMapping[str, typing.Any]] = kwargs.get('sorting', None)
        filtering: typing.Optional[collections.MutableMapping[str, typing.Any]] = kwargs.get('filtering', None)
        searching: typing.Optional[collections.MutableMapping[str, typing.Any]] = kwargs.get('searching', None)
        fields: typing.Optional[collections.MutableMapping[str, typing.Any]] = kwargs.get('fields', None)

        params: dict[str, typing.Any] = {}

        if sorting:
            params |= sorting
        if filtering:
            params |= filtering
        if searching:
            params |= searching
        if fields:
            params |= fields

        response: typing.List[typing.Dict[str, typing.Any]] = typing.cast(typing.List[typing.Dict[str, typing.Any]], self._get(
            endpoint='a.json',
            response_data_key='accounts',
            params=params
        ))

        return [Account.from_json(api_client=self, json_data=account) for account in response]
    
    def get_account(
            self,
            account_id: str,
            **kwargs
    ) -> Account:
        """
        Get an account by ID.
        """
        fields: typing.Optional[collections.MutableMapping[str, typing.Any]] = kwargs.get('fields', None)
        params: dict[str, typing.Any] = {}

        if fields:
            params |= fields

        return Account.from_json(
            api_client=self, 
            json_data=typing.cast(typing.Dict[str, typing.Any],self._get(
                endpoint='a',
                response_data_key='accounts',
                path=f'/{account_id}.json',
                params=params,
                pagination_type='NONE'
            ))
        )
    