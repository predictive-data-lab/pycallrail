from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING, ClassVar
import datetime as dt
from enum import Enum

if TYPE_CHECKING:
    from ..callrail import *

from api.accounts import *

class TextMessage:
    """ A text message. """
    parent: ClassVar[TextMessageThread]
    
    direction: str
    content: str
    created_at: dt.datetime

    def __init__(self, parent: TextMessageThread, data: Dict[str, Any]):
        self.parent = parent
        if data is not None:
            self.as_dict = data
            self.__extract_from_data()

    def __extract_from_data(self) -> None:
        self.direction = self.as_dict.get('direction')
        self.content = self.as_dict.get('content')
        self.created_at = dt.datetime.fromisoformat(self.as_dict.get('created_at'))



class TextMessageThread:
    """
    A text message thread.
    """
    parent: ClassVar[Account]

    id: str
    company_id: str
    initial_tracker_id: str
    current_tracker_id: str
    customer_name: str
    customer_phone_number: str
    initial_tracking_number: str
    current_tracking_number: str
    last_message_at: dt.datetime
    state: str
    company_time_zone: str
    formatted_customer_phone_number: str
    formatted_initial_tracking_number: str
    formatted_current_tracking_number: str
    formatted_customer_name: str
    recent_messages: List[TextMessage]
    lead_status: str

    def __init__(self, parent: Account, data: Dict[str, Any]):
        self.parent = parent
        if data is not None:
            self.as_dict = data
            self.__extract_from_data()

    def __extract_from_data(self):
        self.id = self.as_dict.get('id')
        self.company_id = self.as_dict.get('company_id')
        self.initial_tracker_id = self.as_dict.get('initial_tracker_id')
        self.current_tracker_id = self.as_dict.get('current_tracker_id')
        self.customer_name = self.as_dict.get('customer_name')
        self.customer_phone_number = self.as_dict.get('customer_phone_number')
        self.initial_tracking_number = self.as_dict.get('initial_tracking_number')
        self.current_tracking_number = self.as_dict.get('current_tracking_number')
        self.last_message_at = dt.datetime.fromisoformat(self.as_dict.get('last_message_at'))
        self.state = self.as_dict.get('state')
        self.company_time_zone = self.as_dict.get('company_time_zone')
        self.formatted_customer_phone_number = self.as_dict.get('formatted_customer_phone_number')
        self.formatted_initial_tracking_number = self.as_dict.get('formatted_initial_tracking_number')
        self.formatted_current_tracking_number = self.as_dict.get('formatted_current_tracking_number')
        self.formatted_customer_name = self.as_dict.get('formatted_customer_name')
        self.recent_messages = [TextMessage(self, message) for message in self.as_dict.get('recent_messages')]
        self.lead_status = self.as_dict.get('lead_status')

    def send_text_message(
            self,
            data: dict
    ) -> TextMessageThread:
        """
        Send a text message to a customer.
        """
        account_id = self.parent.id

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
            
        
        text_thread= self.parent.parent._post(
            endpoint='a',
            path=f'/{account_id}/text-messages.json',
            data=data
        )

        return TextMessageThread(self.parent, text_thread)
    
    def archive(
            self
    ):
        """Archive the text message thread."""
        account_id = self.parent.id

        if self.parent.parent.request_delay:
            time.sleep(self.parent.parent.request_delay)
        
        self.parent.parent._put(
            endpoint='a',
            path=f'/{account_id}/text-messages/{self.id}/archive.json',
            data = {'state': 'archived'}
        )