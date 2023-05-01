from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING, ClassVar, cast
import datetime as dt
from dateutil import parser
from enum import Enum

if TYPE_CHECKING:
    from ..callrail import *

from pycallrail.api.accounts import *

class TextMessage:
    """ A text message. """
    parent: TextMessageThread
    
    direction: str
    content: str
    created_at: dt.datetime

    def __init__(self, parent: TextMessageThread, data: Dict[str, Any]) -> None:
        if not isinstance(parent, TextMessageThread):
            raise TypeError
        self.parent = parent
        self.as_dict: Dict[str, Any] = data
        self.__extract_from_data()

    def __extract_from_data(self) -> None:
        # throw a key error if the data is missing any of the required keys
        
        if not all(key in self.as_dict for key in ['direction', 'content', 'created_at']):
            raise KeyError
        
        # validate the direction
        if self.as_dict.get('direction') not in ['inbound', 'outbound']:
            raise ValueError('direction must be inbound or outbound')
        
        self.direction = cast(str, self.as_dict.get('direction'))
        self.content = cast(str,self.as_dict.get('content'))
        self.created_at = dt.datetime.fromisoformat(cast(str,self.as_dict.get('created_at')))



class TextMessageThread:
    """
    A text message thread.
    """
    parent: Account

    id: str
    company_id: str
    initial_tracker_id: str
    current_tracker_id: str
    customer_name: str
    customer_phone_number: str
    initial_tracking_number: str
    current_tracking_number: str
    last_message_at: Optional[dt.datetime]
    state: str
    company_time_zone: str
    formatted_customer_phone_number: str
    formatted_initial_tracking_number: str
    formatted_current_tracking_number: str
    formatted_customer_name: str
    recent_messages: List[TextMessage]
    lead_status: str

    def __init__(self, parent: Account, data: Dict[str, Union[str, list[dict]]]) -> None:
        self.parent = parent
        self.as_dict: Dict[str, Union[str, list[dict]]] = data
        self.__extract_from_data()

    def __extract_from_data(self) -> None:

        self.id = cast(str,self.as_dict.get('id'))
        self.company_id = cast(str,self.as_dict.get('company_id'))
        self.initial_tracker_id = cast(str,self.as_dict.get('initial_tracker_id'))
        self.current_tracker_id = cast(str,self.as_dict.get('current_tracker_id'))
        self.customer_name = cast(str,self.as_dict.get('customer_name'))
        self.customer_phone_number = cast(str,self.as_dict.get('customer_phone_number'))
        self.initial_tracking_number = cast(str,self.as_dict.get('initial_tracking_number'))
        self.current_tracking_number = cast(str,self.as_dict.get('current_tracking_number'))
        self.last_message_at = parser.parse(cast(str,self.as_dict.get('last_message_at'))) if self.as_dict.get('last_message_at') else None
        self.state = cast(str,self.as_dict.get('state'))
        self.company_time_zone = cast(str,self.as_dict.get('company_time_zone'))
        self.formatted_customer_phone_number = cast(str,self.as_dict.get('formatted_customer_phone_number'))
        self.formatted_initial_tracking_number = cast(str,self.as_dict.get('formatted_initial_tracking_number'))
        self.formatted_current_tracking_number = cast(str,self.as_dict.get('formatted_current_tracking_number'))
        self.formatted_customer_name = cast(str,self.as_dict.get('formatted_customer_name'))
        self.recent_messages = [TextMessage(self, message) for message in cast(list[dict],self.as_dict.get('recent_messages'))]
        self.lead_status = cast(str,self.as_dict.get('lead_status'))

    def send_text_message(
            self,
            data: dict
    ) -> TextMessageThread:
        """
        Send a text message to a customer.
        """
        account_id: str = self.parent.id

        if self.parent.parent.request_delay:
            time.sleep(self.parent.parent.request_delay)
        
        for key in [
            'company_id',
            'tracking_number',
            'customer_phone_number',
            'content'
        ]:
            if key not in data:
                raise ValueError(f'Key "{key}" is required.')
            if not data[key]:
                raise ValueError(f'Key "{key}" cannot be empty.')
            for dict_key in data:
                if dict_key not in [
                    'company_id',
                    'tracking_number',
                    'customer_phone_number',
                    'content'
                ]:
                    raise ValueError(f'Key "{dict_key}" is not valid.')
            
        
        text_thread: Dict[str, Any]= cast(Dict[str, Any],self.parent.parent._post(
            endpoint='a',
            path=f'/{account_id}/text-messages.json',
            data=data
        ))

        return TextMessageThread(self.parent, text_thread)
    
    def archive(
            self
    ) -> None:
        """Archive the text message thread."""
        account_id: str = self.parent.id

        if self.parent.parent.request_delay:
            time.sleep(self.parent.parent.request_delay)
        
        self.parent.parent._put(
            endpoint='a',
            path=f'/{account_id}/text-messages/{self.id}/archive.json',
            data = {'state': 'archived'}
        )