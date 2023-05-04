from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pycallrail.base as base
import pycallrail.callrail as crl
import typing
import typing_extensions
import requests


class Call(base.CallRailBase):
    """
    Represents a CallRail call.
    
    More information: https://apidocs.callrail.com/#calls
    """

    # These fields are always returned by the API
    answered: bool
    business_phone_number: typing.Optional[str]
    customer_city: str
    customer_country: str
    customer_name: str
    customer_phone_number: str
    customer_state: str
    direction: str
    duration: int
    id: str
    recording: typing.Optional[str]
    recording_duration: typing.Optional[str]
    recording_player: typing.Optional[str]
    start_time: dt.datetime
    tracking_phone_number: str
    voicemail: bool
    
    # User Requested Fields
    call_type: typing.Optional[str]
    company_id: typing.Optional[str]
    company_name: typing.Optional[str]
    company_time_zone: typing.Optional[str]
    created_at: typing.Optional[str]
    device_type: typing.Optional[str]
    first_call: typing.Optional[bool]
    formatted_call_type: typing.Optional[str]
    formatted_customer_location: typing.Optional[str]
    formatted_business_phone_number: typing.Optional[str]
    formatted_customer_name: typing.Optional[str]
    prior_calls: typing.Optional[int]
    formatted_customer_name_or_phone_number: typing.Optional[str]
    formatted_customer_phone_number: typing.Optional[str]
    formatted_duration: typing.Optional[str]
    formatted_tracking_phone_number: typing.Optional[str]
    formatted_tracking_source: typing.Optional[str]
    formatted_value: typing.Optional[str]
    good_lead_call_id: typing.Optional[int]
    good_lead_call_time: typing.Optional[str]
    lead_status: typing.Optional[str]
    note: typing.Optional[str]
    source: typing.Optional[str]
    source_name: typing.Optional[str]
    tags: typing.Optional[typing.List[typing.Any]]
    total_calls: typing.Optional[int]
    value: typing.Optional[str]
    waveforms: typing.Optional[typing.List[typing.Any]]
    tracker_id: typing.Optional[str]
    speaker_percent: typing.Optional[typing.Dict[str, typing.Any]]
    keywords: typing.Optional[str]
    medium: typing.Optional[str]
    campaign: typing.Optional[str]
    referring_url: typing.Optional[str]
    landing_page_url: typing.Optional[str]
    last_requested_url: typing.Optional[str]
    referrer_domain: typing.Optional[str]
    utm_source: typing.Optional[str]
    utm_medium: typing.Optional[str]
    utm_term: typing.Optional[str]
    utm_content: typing.Optional[str]
    utm_campaign: typing.Optional[str]
    utma: typing.Optional[str]
    utmb: typing.Optional[str]
    utmc: typing.Optional[str]
    utmv: typing.Optional[str]
    utmz: typing.Optional[str]
    ga: typing.Optional[str]
    gclid: typing.Optional[str]
    fbclid: typing.Optional[str]
    msclkid: typing.Optional[str]
    milestones: typing.Optional[typing.Any]
    timeline_url: typing.Optional[str]
    keywords_spotted: typing.Optional[typing.List[typing.Any]]
    call_highlights: typing.Optional[typing.List[typing.Any]]
    agent_email: typing.Optional[str]
    keypad_entries: typing.Optional[typing.MutableMapping[str, typing.Any]]


    def __init__(
            self,
            api_client: crl.CallRail,
            account_id: str,
            **kwargs
    ) -> None:
        super(Call, self).__init__()
        self.api_client: crl.CallRail = api_client
        self.account_id: str = account_id

        for key, value in kwargs.items():
            if key not in self.__class__.__annotations__.keys():
                raise AttributeError(f'{key} is not a valid attribute for {self.__class__.__name__}.')
            else:
                setattr(self, key, value)
    
    @classmethod
    def from_json(
        cls,
        api_client: crl.CallRail,
        account_id: str,
        json_data: typing.Dict[str, typing.Any]
    ) -> Call:
        """
        Deserialize JSON data to a Call object.
        
        :param api_client: The CallRail API client.
        :param json_data: The JSON data to deserialize.
        """

        # first lets convert the start_time to a datetime
        json_data['start_time'] = dateparser.parse(json_data['start_time'])

        return cls(api_client, account_id, **json_data)
    
    
    def update(
            self, 
            tags: typing.Optional[typing.List[typing.Any]] = None,
            note: typing.Optional[str] = None,
            value: typing.Optional[str] = None,
            lead_status: typing.Optional[str] = None,
            append_tags: typing.Optional[bool] = None,
            customer_name: typing.Optional[str] = None,
            spam: typing.Optional[bool] = None
        ) -> None:
        """
        Update a Call object.
        More information: https://apidocs.callrail.com/#updating-a-call
        """
        # update the attributes
        if append_tags and tags and hasattr(self, 'tags'):
            self.tags.extend(tags) # type: ignore
        else:
            self.tags = tags
        if note:
            self.note = note
        if value:
            self.value = value
        if lead_status:
            self.lead_status = lead_status
        if customer_name:
            self.customer_name = customer_name
        if spam:
            self.spam = spam

        # form the request body
        body: typing.Dict[str, typing.Any] = {
            'tags': tags,
            'note': note,
            'value': value,
            'lead_status': lead_status,
            'append_tags': append_tags,
            'customer_name': customer_name,
            'spam': spam
        }

        # send the request
        response_data: typing.Dict[str, typing.Any] = typing.cast(
            typing.Dict[str, typing.Any], 
            self.api_client._put(
                endpoint = f'a/{self.account_id}',
                path=f'calls/{self.id}.json',
                data=body
            )
        )

        # update the attributes
        for key, value in response_data.items():
            # raise an error if the attribute doesn't exist
            if key not in self.__class__.__annotations__.keys():
                raise AttributeError(f'{key} is not a valid attribute for {self.__class__.__name__}.')
            else:
                setattr(self, key, value)
        
        
        

    def get_recording(self) -> typing.Union[bytes, None]:
        """
        Get the recording of the call.
        More information: https://apidocs.callrail.com/#get-the-recording-of-the-call

        If no recording exists, None is returned.
        """
        if self.recording:
            with self.api_client.session.get(url=self.recording) as response:
                return response.content
        else:
            return None