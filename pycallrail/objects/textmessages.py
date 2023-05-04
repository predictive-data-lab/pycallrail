from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pycallrail.base as base
import pycallrail.callrail as crl
import typing
import logging
import typeguard

class TextMessage(base.CallRailBase):
    """
    Represents a TextMessage.
    More information: https://apidocs.callrail.com/#text-messages
    """
    
    direction: str
    content: str
    created_at: dt.datetime

    def __init__(
        self,
        direction: str,
        content: str,
        created_at: dt.datetime
    ) -> None:
        super(TextMessage, self).__init__()
        if direction not in ["incoming", "outgoing"]:
            raise ValueError("direction must be 'incoming' or 'outgoing'")
        self.direction = direction
        if created_at is None or not isinstance(created_at, dt.datetime):
            raise ValueError("created_at must be a datetime")
        self.created_at = created_at
        self.content = content

class TextMessageConversation(base.CallRailBase):
    """
    A conversation/thread of text messages.
    More information: https://apidocs.callrail.com/#text-messages
    """
    
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
    recent_messages: typing.List[TextMessage]

    # saw these fields appear in testing, but not in the docs
    tracker_name: typing.Optional[str]
    company_name: typing.Optional[str]

    # Optional User Requested Fields
    lead_status: typing.Optional[str]

    def __init__(
        self,
        api_client: crl.CallRail,
        account_id: str,
        **kwargs
    ) -> None:
        super(TextMessageConversation, self).__init__()
        self.api_client = api_client
        self.account_id = account_id

        # validate id is in kwargs
        if 'id' not in kwargs.keys():
            raise KeyError("id is a required argument")
        
        for k,v in kwargs.items():
            # validate its a valid attribute
            if k not in self.__class__.__annotations__.keys():
                raise AttributeError(f"{k} is not a valid attribute for {self.__class__.__name__}")
            else:
                setattr(self, k, v)

    @classmethod
    def from_json(
        cls,
        api_client: crl.CallRail,
        account_id: str,
        json_data: typing.Dict[str, typing.Any]
    ) -> TextMessageConversation:
        """
        Deserialize JSON to a Text Message Conversation
        """

        json_data['last_message_at'] = dateparser.parse(json_data['last_message_at'])

        json_data['recent_messages'] = [
            TextMessage(
                message['direction'],
                message['content'],
                dateparser.parse(message['created_at'])
            ) for message in json_data['recent_messages']
        ]

        return cls(
            api_client=api_client,
            account_id=account_id,
            **json_data
        )

    def archive(self, state: str = 'archived') -> None:
        """
        Archive the conversation
        """
        self.api_client._put(
            endpoint=f'a/{self.account_id}',
            path=f'text-messages/{self.id}.json',
            params={
                'conversation_id': self.id
            },
            data = {
                'state': state
            }
        )

        self.state = state