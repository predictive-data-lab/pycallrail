from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
import logging
import datetime as dt

if TYPE_CHECKING:
    from ..callrail import CallRail

from callrail import *
from .call import *
from .tag import *
from .companies import *
from .form_submissions import *
from .textmessage import *

class Account:
    """
    Represents an account in CallRail
    """
    parent: CallRail
    id: str
    name: str
    outbound_recording_enabled: bool
    hipaa_account: bool
    numeric_id: Optional[int]

    def __init__(
            self,
            data: Optional[dict],
            parent: CallRail):
        self.parent = parent
        if data is not None:
            self.as_dict = data
            self.__extract_from_data()

    def __extract_from_data(self):
        self.id = self.as_dict.get("id")
        self.name = self.as_dict.get("name")
        self.outbound_recording_enabled = self.as_dict.get("outbound_recording_enabled")
        self.hipaa_account = self.as_dict.get("hipaa_account")
        self.numeric_id = self.as_dict.get("numeric_id", None)

    # since calls are under the account endpoint, lets make it possible to CRUD calls from the account object
    def create_call(
        self,
        call_data: dict,
    ):
        """
        Create a call.
        """
        account_id = self.id

        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)

        for key in [
            'caller_id',
            'customer_phone_number',
            'business_phone_number',
            'recording_enabled',
            'outbound_greeting_recording_url',
            'outbound_greeting_text',
            'agent_id'
        ]:
            if key not in call_data:
                raise ValueError(f'Data must include {key}.')
            if call_data[key] is None:
                raise ValueError(f'Data must include {key}.')
            for dict_key in call_data:
                if dict_key not in [
                    'caller_id',
                    'customer_phone_number',
                    'business_phone_number',
                    'recording_enabled',
                    'outbound_greeting_recording_url',
                    'outbound_greeting_text',
                    'agent_id'
                ]:
                    raise ValueError(f'Invalid key {dict_key} in call_data.')

        call_json = self.parent._post(
            endpoint = 'a',
            path = f'/{account_id}/calls.json',
            data = call_data
        )

        return Call(call_json, parent=self)
    
    def list_calls(
        self,
        company_id: str = None,
        tracker_id: str = None,
        **kwargs
    ):    # sourcery skip: remove-none-from-default-get
        """
        List calls for an account.
        """
        account_id = self.id

        pagination_type: PaginationType = kwargs.get('pagination_type', PaginationType.RELATIVE)

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

        if company_id:
            params['company_id'] = company_id
        if tracker_id:
            params['tracker_id'] = tracker_id

        calls = self.parent._get(
            endpoint='a',
            path=f'/{account_id}/calls.json',
            params=params,
            response_data_key='calls',
            pagination_type=pagination_type
        )

        if isinstance(calls, list) and len(calls) == 1:
            return Call(calls[0], parent=self)
        elif isinstance(calls, list):
            return [Call(call, parent=self) for call in calls]
        elif isinstance(calls, dict):
            return Call(calls, parent=self)
    
    def get_call(
        self,
        call_id: str,
        **kwargs
    ):
        """
        Get a call.
        """
        obj_or_dict = kwargs.get('obj_or_dict', 'obj')

        account_id = self.id

        fields: dict = kwargs.get('fields', None)

        params = {}

        if fields:
            params |= fields

        call: dict = self.parent._get(
            endpoint='a',
            path=f'/{account_id}/calls/{call_id}.json',
            params=params,
            response_data_key='call'
        )

        if obj_or_dict == 'dict':
            return call
        
        elif obj_or_dict == 'obj':
            return Call(call, parent=self) if isinstance(call, dict) else None


    ##############################
    # TAGS
    ##############################

    def list_tags(
            self,
            company_id: str = None,
            status: str = None,
            tag_level: str = None,
            **kwargs
    ):
        """
        List tags for an account.
        """
        account_id = self.id

        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)
        
        sorting = kwargs.get('sorting', None)


        params = {}
        
        if sorting:
            params |= sorting
        if company_id:
            params['company_id'] = company_id
        if status:
            params['status'] = status
        if tag_level:
            params['tag_level'] = tag_level

        tags = self.parent._get(
            endpoint='a',
            path=f'/{account_id}/tags.json',
            params=params,
            response_data_key='tags'
        )

        if isinstance(tags, list) and len(tags) == 1:
            return Tag(tags[0], parent=self)
        
        elif isinstance(tags, list):
            return [Tag(tag, parent=self) for tag in tags]
        
        elif isinstance(tags, dict):
            return Tag(tags, parent=self)

        else:
            return None

    def create_tag(
            self,
            data: dict,
    ):
        """
        Create a tag.
        """
        account_id = self.id

        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)

        for key in [
            'name'
        ]:
            if key not in data:
                raise ValueError(f'Data must include {key}.')
            if data[key] is None:
                raise ValueError(f'Data must include {key}.')
    

        tag_json = self.parent._post(
            endpoint='a',
            path=f'/{account_id}/tags.json',
            data=data
        )

        return Tag(tag_json, parent=self)
    
    ##############################
    # Companies
    ##############################

    def list_companies(
            self,
            **kwargs
    ):
        """
        List companies for an account.
        """
        account_id = self.id

        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)
        
        sorting = kwargs.get('sorting', None)
        filtering = kwargs.get('filtering', None)
        searching = kwargs.get('searching', None)


        params = {}
        
        if sorting:
            params |= sorting
        if filtering:
            params |= filtering
        if searching:
            params |= searching

        companies = self.parent._get(
            endpoint='a',
            path=f'/{account_id}/companies.json',
            params=params,
            response_data_key='companies'
        )

        if isinstance(companies, list) and len(companies) > 1:
            return [Company(company, parent=self) for company in companies]
        
        elif isinstance(companies, list) and len(companies) == 1:
            return Company(companies[0], parent=self)
        
        elif isinstance(companies, dict):
            return Company(companies, parent=self)
        
        else:
            return None

    def get_company(
            self,
            company_id: str,
            **kwargs
    ):
        
        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)
        
        account_id = self.id

        obj_or_dict = kwargs.get('obj_or_dict', 'obj')
        """ONLY SPECIFY IF YOU WANT A DICT BACK INSTEAD OF AN OBJECT - USED INTERNALLY TO REFRESH OBJECTS WITHOUT CREATING A NEW OBJECT"""

        company: dict = self.parent._get(
            endpoint='a',
            path=f'/{account_id}/companies/{company_id}.json'
        )

        if obj_or_dict == 'dict':
            return company
        
        elif obj_or_dict == 'obj':
            return Company(company, parent=self) if isinstance(company, dict) else None
        
    def create_company(
            self,
            data: dict
    ):
        """
        Create a company.
        """
        account_id = self.id

        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)

        for key in [
            'name'
        ]:
            if key not in data:
                raise ValueError(f'Data must include {key}.')
            if data[key] is None:
                raise ValueError(f'Data must include {key}.')
    

        company_json: dict = self.parent._post(
            endpoint='a',
            path=f'/{account_id}/companies.json',
            data=data
        )

        return Company(company_json, parent=self)
    
    ##############################
    # Form Submissions
    ##############################

    def list_form_submissions(
            self,
            **kwargs
    ):  # sourcery skip: remove-none-from-default-get
        """
        List form submissions for an account.
        """
        account_id = self.id

        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)
        
        sorting = kwargs.get('sorting', None)
        filtering = kwargs.get('filtering', None)
        fields = kwargs.get('fields', None)


        params = {}
        
        if sorting:
            params |= sorting
        if filtering:
            params |= filtering
        if fields:
            params |= fields

        form_submissions = self.parent._get(
            endpoint='a',
            path=f'/{account_id}/form_submissions.json',
            params=params,
            response_data_key='form_submissions'
        )

        if isinstance(form_submissions, list) and len(form_submissions) > 1:
            return [FormSubmission(form_submission, parent=self) for form_submission in form_submissions]
        
        elif isinstance(form_submissions, list) and len(form_submissions) == 1:
            return FormSubmission(form_submissions[0], parent=self)
        
        elif isinstance(form_submissions, dict):
            return FormSubmission(form_submissions, parent=self)
        
        else:
            return None
    
    def create_form_submission(
            self,
            data: dict
    ):
        """
        Create a form submission.
        """
        account_id = self.id

        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)

        for key in [
            'company_id',
            'referrer',
            'referring_url',
            'landing_page_url',
            'form_url',
            'form_data'
        ]:
            if key not in data:
                raise ValueError(f'Data must include {key}.')
            if data[key] is None:
                raise ValueError(f'Data must include {key}.')
    

        form_submission_json = self.parent._post(
            endpoint='a',
            path=f'/{account_id}/form_submissions.json',
            data=data
        )

        return FormSubmission(form_submission_json, parent=self)
    
    def ignore_form_fields(
            self,
            data: dict
    ):
        """
        Ignore form fields.
        """
        account_id = self.id

        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)

        for key in [
            'company_ids',
            'field_names'
        ]:
            if key not in data:
                raise ValueError(f'Data must include {key}.')
            if data[key] is None:
                raise ValueError(f'Data must include {key}.')
    

        self.parent._post(
            endpoint='a',
            path=f'/{account_id}/form_submissions/ignore_fields.json',
            data=data
        )

    ##############################
    # Text Messages
    ##############################

    def list_text_message_threads(
            self,
            company_id: str,
            **kwargs
    ):
        """
        List text message threads for an account.
        """
        account_id = self.id

        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)
        
        searching = kwargs.get('searching', None)
        filtering = kwargs.get('filtering', None)
        fields = kwargs.get('fields', None)


        params = {}
        
        if searching:
            params |= sorting
        if filtering:
            params |= filtering
        if fields:
            params |= fields

        text_message_threads = self.parent._get(
            endpoint='a',
            path = f'/{account_id}/text-messages.json',
            params=params,
            response_data_key = 'conversations'
        )

        if isinstance(text_message_threads, list) and len(text_message_threads) > 1:
            return [TextMessageThread(text_message_thread, parent=self) for text_message_thread in text_message_threads]
        if isinstance(text_message_threads, list) and len(text_message_threads) == 1:
            return TextMessageThread(text_message_threads[0], parent=self)
        if isinstance(text_message_threads, dict):
            return TextMessageThread(text_message_threads, parent=self)
        else:
            return None
        
    def get_text_message_thread(
        self,
        thread_id: str,
        **kwargs
    ):
        """
        Get a text message thread.
        """

        account_id = self.id
        fields = kwargs.get('fields', None)

        if self.parent.request_delay:
            time.sleep(self.parent.request_delay)
        
        params = {}

        if fields:
            params |= fields

        text_message_thread = self.parent._get(
            endpoint='a',
            path = f'/{account_id}/text-messages/{thread_id}.json',
            params=params
        )

        return TextMessageThread(text_message_thread, parent=self)

        
            


######################################################

    def __dict__(self) -> Dict[str, Any]:
        if self.numeric_id is not None:
            return {
                "id": self.id,
                "name": self.name,
                "outbound_recording_enabled": self.outbound_recording_enabled,
                "hipaa_account": self.hipaa_account,
                "numeric_id": self.numeric_id
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "outbound_recording_enabled": self.outbound_recording_enabled,
                "hipaa_account": self.hipaa_account
            }

    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"Account: {self.name}"