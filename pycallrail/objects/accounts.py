from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pycallrail.base as base
import pycallrail.callrail as crl
import pycallrail.objects.calls as calls
import pycallrail.objects.tags as tags
import pycallrail.objects.companies as companies
import pycallrail.objects.form_submissions as forms
import pycallrail.objects.textmessages as messages
import typing
import logging

class Account(base.CallRailBase):
    """
    Represents a CallRail Account. Class should preferably not be instantiated directly.

    More information: https://apidocs.callrail.com/#accounts
    """

    id: str
    name: str
    outbound_recording_enabled: bool
    hipaa_account: bool

    # Optional User Requested Fields
    numeric_id: typing.Optional[int]

    def __init__(
            self,
            api_client: crl.CallRail,
            id: str,
            name: str,
            outbound_recording_enabled: bool,
            hipaa_account: bool,
            numeric_id: typing.Optional[int] = None
    ) -> None:
        super(Account, self).__init__()
        self.api_client: crl.CallRail = api_client
        self.id = id
        self.name = name
        self.outbound_recording_enabled = outbound_recording_enabled
        self.hipaa_account = hipaa_account

        if numeric_id:
            self.numeric_id = numeric_id

    @classmethod
    def from_json(
        cls,
        api_client: crl.CallRail,
        json_data: typing.Dict[str, typing.Any]
    ) -> Account:
        """
        Deserialize JSON data into an Account object.
        
        :api_client: CallRail API object
        :json_data: JSON data
        """

        account = Account(
            api_client=api_client,
            id=json_data['id'],
            name=json_data['name'],
            outbound_recording_enabled=json_data['outbound_recording_enabled'],
            hipaa_account=json_data['hipaa_account']
        )

        if 'numeric_id' in json_data:
            account.numeric_id = json_data['numeric_id']

        return account
    
    #########################
    # Calls
    #########################

    def list_calls(
            self,
            **kwargs
        ) -> typing.Union[typing.List[calls.Call], None]:
        """
        List all calls associated with this account.

        Keyword args acceptable include: Pagination Type, Sorting, Filtering, Field Selection, and Searching.
        Defaults to relative pagination.
        
        More info: https://apidocs.callrail.com/#listing-all-calls
        """

        pagination_type: str = kwargs.get('pagination_type', 'RELATIVE')

        sorting = kwargs.get('sorting', None)
        filtering = kwargs.get('filtering', None)
        searching = kwargs.get('searching', None)
        fields = kwargs.get('fields', None)

        params = {}

        if sorting:
            params['sorting'] = sorting
        if filtering:
            params['filtering'] = filtering
        if searching:
            params['searching'] = searching
        if fields:
            params['fields'] = fields

        if calls_response := typing.cast(
            typing.Union[typing.List[typing.Dict[str, typing.Any]], None],
            self.api_client._get(
                endpoint=f'a/{self.id}',
                response_data_key='calls',
                path='calls.json',
                params=params or None,
                pagination_type=pagination_type,
            ),
        ):
            return [calls.Call.from_json(self.api_client, self.id, call) for call in calls_response]
        else:
            return None

    def get_call(
        self,
        call_id: str,
        fields: typing.Optional[typing.MutableMapping[str, typing.Union[str, typing.Any]]] = None
    ) -> calls.Call:
        """
        Retrieve a single call by ID.
        
        Field selection is supported by this method.
        
        More info: https://apidocs.callrail.com/#retrieving-a-single-call
        """

        if fields:
            data = self.api_client._get(
                endpoint=f'a/{self.id}',
                path=f'calls/{call_id}.json',
                params=fields
            )
        else:
            data = self.api_client._get(
                endpoint=f'a/{self.id}',
                path=f'calls/{call_id}.json'
            )

        return calls.Call.from_json(
            self.api_client, 
            self.id, 
            typing.cast(typing.Dict[str, typing.Any], data)
        )
    
    def create_call(
            self,
            caller_id: int,
            customer_phone_number: str,
            business_phone_number: str,
            recording_enabled: typing.Optional[bool] = None,
            outbound_greeting_recording_url: typing.Optional[str] = None,
            outbound_greeting_text: typing.Optional[str] = None,
            agent_id: typing.Optional[str] = None
    ) -> calls.Call:
        """
        Create a new call.
        
        This method is rate limited. There is no functionality to currently check for rate limits. Be careful!
        More info: https://apidocs.callrail.com/#creating-an-outbound-phone-call
        """

        logging.warning('This method is rate limited. There is no functionality to currently check for rate limits. Be careful!')

        body = {
            'caller_id': caller_id,
            'customer_phone_number': customer_phone_number,
            'business_phone_number': business_phone_number
        }

        

        if recording_enabled:
            body['recording_enabled'] = recording_enabled
        if outbound_greeting_recording_url:
            body['outbound_greeting_recording_url'] = outbound_greeting_recording_url
        if outbound_greeting_text:
            body['outbound_greeting_text'] = outbound_greeting_text
        if agent_id:
            body['agent_id'] = agent_id
        
        data = self.api_client._post(
            endpoint=f'a/{self.id}',
            path='calls.json',
            data=body
        )

        return calls.Call.from_json(
            self.api_client,
            self.id,
            typing.cast(typing.Dict[str, typing.Any], data)
        )
    
    #########################
    # Tags
    #########################

    def list_tags(
            self,
            **kwargs
    ) -> typing.Union[typing.List[tags.Tag], None]:
        """
        This endpoint returns a paginated array of tags within the target account.

        More info: https://apidocs.callrail.com/#retrieving-all-tags
        """

        pagination_type: str = kwargs.get('pagination_type', 'RELATIVE')

        sorting = kwargs.get('sorting', None)

        params = {}

        if sorting:
            params['sorting'] = sorting

        if tags_response := typing.cast(
            typing.List[typing.Dict[str, typing.Any]],
            self.api_client._get(
                endpoint=f'a/{self.id}',
                response_data_key='tags',
                path='tags.json',
                params=params or None,
                pagination_type=pagination_type,
            )
        ):
            return [tags.Tag.from_json(self.api_client, self.id, tag) for tag in tags_response]

        else:
            return None
        
    def create_tag(
            self,
            name: str,
            company_id: typing.Optional[str] = None,
            color: typing.Optional[str] = None,
            tag_level: typing.Optional[str] = None
    ) -> tags.Tag:
        """
        Create a new tag.
        
        More info: https://apidocs.callrail.com/#creating-a-tag
        """

        # some validation before sending the request
        if not name:
            raise ValueError('name is required')

        if tag_level == 'company' and not company_id:
            raise ValueError('company_id is required if tag_level is company or not "account"')

        body = {
            'name': name
        }

        if company_id:
            body['company_id'] = company_id
        if color:
            body['color'] = color
        if tag_level:
            body['tag_level'] = tag_level

        data = self.api_client._post(
            endpoint=f'a/{self.id}',
            path='tags.json',
            data=body
        )

        return tags.Tag.from_json(
            self.api_client,
            self.id,
            typing.cast(typing.Dict[str, typing.Any], data)
        )
    
    #########################
    # Companies
    #########################

    def list_companies(
            self,
            **kwargs
    ) -> typing.Union[typing.List[companies.Company], None]:
        """
        List all companies under account scope.

        More info: https://apidocs.callrail.com/#creating-a-company
        """

        pagination_type: str = kwargs.get('pagination_type', 'RELATIVE')

        sorting = kwargs.get('sorting', None)
        filtering: typing.Dict[str, typing.Any] = typing.cast(typing.Dict[str, typing.Any], kwargs.get('filtering', None))
        searching = kwargs.get('searching', None)

        if filtering:
            # only filtering field supported is status, raise a ValueError if there is a other field
            for k,v in filtering.items():
                if k != 'status':
                    raise ValueError(f'filtering field {k} is not supported')

        params = {}

        if sorting:
            params['sorting'] = sorting
        if filtering:
            params['filtering'] = filtering
        if searching:
            params['searching'] = searching

        if companies_response := typing.cast(
            typing.List[typing.Dict[str, typing.Any]],
            self.api_client._get(
                endpoint=f'a/{self.id}',
                response_data_key='companies',
                path='companies.json',
                params=params or None,
                pagination_type=pagination_type,
        )):
            return [companies.Company.from_json(self.api_client, self.id, company) for company in companies_response]
        else:
            return None
        
    def get_company(
            self,
            company_id: str,
            fields: typing.Optional[typing.MutableMapping[str, str]] = None
    ) -> companies.Company:
        """
        Get a company.
        
        More info: https://apidocs.callrail.com/#retrieving-a-single-company
        """

        if fields:
            data = self.api_client._get(
                endpoint=f'a/{self.id}',
                path=f'companies/{company_id}.json',
                params=fields
            )
        else:
            data = self.api_client._get(
                endpoint=f'a/{self.id}',
                path=f'companies/{company_id}.json'
            )

        return companies.Company.from_json(
            self.api_client,
            self.id,
            typing.cast(typing.Dict[str, typing.Any], data)
        )
    
    def create_company(
            self,
            name: str,
            time_zone: typing.Optional[str] = None
    ) -> companies.Company:
        """
        Create a new company.
        
        More info: https://apidocs.callrail.com/#creating-a-company
        """

        body = {
            'name': name
        }

        if time_zone:
            body['time_zone'] = time_zone

        data = self.api_client._post(
            endpoint=f'a/{self.id}',
            path='companies.json',
            data=body
        )

        return companies.Company.from_json(
            self.api_client,
            self.id,
            typing.cast(typing.Dict[str, typing.Any], data)
        )

    #########################
    # Form Submissions
    #########################

    def list_form_submissions(
            self,
            **kwargs
    ) -> typing.Union[typing.List[forms.FormSubmission], None]:
        """
        List form submissions.

        More information: https://apidocs.callrail.com/#listing-all-form-submissions
        """

        pagination_type: str = kwargs.get('pagination_type', 'RELATIVE')

        sorting = kwargs.get('sorting', None)
        filtering = kwargs.get('filtering', None)
        fields = kwargs.get('fields', None)

        params = {}

        if sorting:
            params['sorting'] = sorting
        if filtering:
            params['filtering'] = filtering
        if fields:
            params['fields'] = fields

        if forms_response := typing.cast(
            typing.List[typing.Dict[str, typing.Any]],
            self.api_client._get(
                endpoint=f'a/{self.id}',
                response_data_key='form_submissions',
                path='form_submissions.json',
                params=params or None,
                pagination_type=pagination_type,
            )
        ):
            return [forms.FormSubmission.from_json(self.api_client, self.id, submission) for submission in forms_response]
        else:
            logging.warning('No form submissions found')
            return None
        
    def create_form_submission(
            self,
            company_id: str,
            referrer: str,
            referring_url: str,
            landing_page_url: str,
            form_url: str,
            form_data: typing.Dict[str, typing.Any]
    ) -> forms.FormSubmission:
        """
        Create a Form Submission.
        
        More information: https://apidocs.callrail.com/#creating-a-form-submission
        """
        body = {
            'company_id': company_id,
            'referrer': referrer,
            'referring_url': referring_url,
            'landing_page_url': landing_page_url,
            'form_url': form_url,
            'form_data': form_data
        }

        data = self.api_client._post(
            endpoint=f'a/{self.id}',
            path='form_submissions.json',
            data=body
        )

        return forms.FormSubmission.from_json(
            self.api_client,
            self.id,
            typing.cast(typing.Dict[str, typing.Any], data)
        )
    
    #########################
    # Text Messages
    #########################

    def list_text_message_conversations(
            self,
            **kwargs
    ) -> typing.Union[typing.List[messages.TextMessageConversation], None]:
        """
        List all text message conversations.
        More information: https://apidocs.callrail.com/#listing-all-conversations
        """
        
        pagination_type: str = kwargs.get('pagination_type', 'RELATIVE')

        sorting = kwargs.get('sorting', None)
        filtering = kwargs.get('filtering', None)
        searching = kwargs.get('searching', None)
        fields = kwargs.get('fields', None)

        params = {}

        if sorting:
            params['sorting'] = sorting
        if filtering:
            params['filtering'] = filtering
        if searching:
            params['searching'] = searching
        if fields:
            params['fields'] = fields


        if text_messages_response := typing.cast(
            typing.List[typing.Dict[str, typing.Any]],
            self.api_client._get(
                endpoint=f'a/{self.id}',
                response_data_key='conversations',
                path='text-messages.json',
                params=params or None,
                pagination_type=pagination_type,
            )
        ):
            return [messages.TextMessageConversation.from_json(self.api_client, self.id, message) for message in text_messages_response]
        else:
            logging.warning('No text messages found')
            return None
        
    def get_text_message_conversation(
            self,
            conversation_id: str,
            fields: typing.Optional[typing.MutableMapping[str, str]] = None
    ) -> messages.TextMessageConversation:
        """
        Retrieve a single text message conversation.
        More information: https://apidocs.callrail.com/#retrieving-a-single-text-conversation
        """

        if fields:
            data = self.api_client._get(
                endpoint=f'a/{self.id}',
                path=f'text-messages/{conversation_id}.json',
                params=fields
            )
        else:
            data = self.api_client._get(
                endpoint=f'a/{self.id}',
                path=f'text-messages/{conversation_id}.json'
            )
        
        return messages.TextMessageConversation.from_json(
            self.api_client,
            self.id,
            typing.cast(typing.Dict[str, typing.Any], data)
        )
        
    def send_text(
            self,
            company_id: str,
            customer_phone_number: str,
            content: str,
            tracking_number: typing.Optional[typing.Union[str, int]] = None
    ) -> messages.TextMessageConversation:
        """
        Send a text message.
        More information: https://apidocs.callrail.com/#sending-a-text-message

        Automated messaging is strictly prohibited by CallRail. This functionality is only for
        use in person to person communication. For example, this method can be used when building a customer service
        portal initiated by a agent. 

        Predictive Data Lab is not to be held responsible for any misuse of this method.
        """
        logging.warning('Sending a text message requires approval from CallRail')
        logging.warning('Endpoint is rate limited! Be careful!')
        logging.warning('Automated messaging is not allowed. Please use this only for use in person to person communication')

        body = {
            'company_id': company_id,
            'customer_phone_number': customer_phone_number,
            'content': content
        }

        if tracking_number:
            body['tracking_number'] = tracking_number # type: ignore

        if len(content) >= 140:
            raise ValueError('Content must be less than 140 characters')
        
        data = self.api_client._post(
            endpoint=f'a/{self.id}',
            path='text-messages.json',
            data=body
        )

        return messages.TextMessageConversation.from_json(
            self.api_client,
            self.id,
            typing.cast(typing.Dict[str, typing.Any], data)
        )