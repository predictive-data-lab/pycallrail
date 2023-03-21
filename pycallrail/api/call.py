from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, ClassVar
import logging
import datetime as dt
from enum import Enum

if TYPE_CHECKING:
    from ..callrail import *

from api.accounts import *

# Enums for Call
class CallType(Enum):
    ABANDONED = "abandoned"
    ANSWERED = "answered"
    IN_PROGRESS = "in_progress"
    MISSED = "missed"
    OUTBOUND = "outbound"
    VOICEMAIL = "voicemail"
    VOICEMAIL_TRANSCRIPTION = "voicemail_transcription"

class Call:
    """
    Represents a CallRail Call
    """
    parent: ClassVar[Account]


    
    answered: bool
    business_phone_number: str
    customer_city: str
    customer_country: str
    customer_name: str
    customer_phone_number: str
    customer_state: str
    direction: str
    duration: int
    id: int
    recording: str
    recording_duration: str
    recording_player: str
    start_time: dt.datetime
    tracking_phone_number: str
    voicemail: bool
    
    # Optional Fields (User Requested)
    call_type: Optional[CallType | str]
    company_id: Optional[str]
    company_name: Optional[str]
    company_time_zone: Optional[str]
    created_at: Optional[dt.datetime]
    device_type: Optional[str]
    first_call: Optional[bool]
    formatted_call_type: Optional[str]
    formatted_customer_location: Optional[str]
    formatted_business_phone_number: Optional[str]
    formatted_duration: Optional[str]
    formatted_tracking_phone_number: Optional[str]
    formatted_tracking_source: Optional[str]
    formatted_value: Optional[str]
    good_lead_call_id: Optional[str]
    lead_status: Optional[str]
    note: Optional[str]
    source: Optional[str]
    source_name: Optional[str]
    tags: Optional[List[str]]
    total_calls: Optional[int]
    value: Optional[str]
    waveforms: Optional[List[str]]
    tracker_id: Optional[str]
    speaker_percent: Optional[dict]
    keywords: Optional[str]
    media: Optional[str]
    campaign: Optional[str]
    referring_url: Optional[str]
    landing_page_url: Optional[str]
    last_requested_url: Optional[str]
    referrer_domain: Optional[str]
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_term: Optional[str]
    utm_content: Optional[str]
    utm_campaign: Optional[str]
    utma : Optional[str]
    utmb : Optional[str]
    utmc : Optional[str]
    utmv : Optional[str]
    utmz : Optional[str]
    ga : Optional[str]
    gclid : Optional[str]
    fbclid : Optional[str]
    msclkid : Optional[str]
    milestones: Optional[dict]
    timeline_url: Optional[str]
    keywords_spotted: Optional[List[str]]
    call_highlights: Optional[List[str]]
    agent_email: Optional[str]
    keypad_entries: Optional[List[str | int]]

    def __init__(
            self,
            data: Optional[dict],
            parent: Account):
        self.parent = parent
        if data is not None:
            self.as_dict = data
            self.__extract_from_data()
        
    def __extract_from_data(self):
        # these are the fields needed to create a Call object
        self.caller_id = self.as_dict.get("caller_id")


        # Optional Fields (User Requested)
        self.call_type = self.as_dict.get("call_type", None)
        self.company_id = self.as_dict.get("company_id", None)
        self.company_name = self.as_dict.get("company_name", None)
        self.company_time_zone = self.as_dict.get("company_time_zone", None)
        self.created_at = self.as_dict.get("created_at", None)
        self.device_type = self.as_dict.get("device_type", None)
        self.first_call = self.as_dict.get("first_call", None)
        self.formatted_call_type = self.as_dict.get("formatted_call_type", None)
        self.formatted_customer_location = self.as_dict.get("formatted_customer_location", None)
        self.formatted_business_phone_number = self.as_dict.get("formatted_business_phone_number", None)
        self.formatted_duration = self.as_dict.get("formatted_duration", None)
        self.formatted_tracking_phone_number = self.as_dict.get("formatted_tracking_phone_number", None)
        self.formatted_tracking_source = self.as_dict.get("formatted_tracking_source", None)
        self.formatted_value = self.as_dict.get("formatted_value", None)
        self.good_lead_call_id = self.as_dict.get("good_lead_call_id", None)
        self.lead_status = self.as_dict.get("lead_status", None)
        self.note = self.as_dict.get("note", None)
        self.source = self.as_dict.get("source", None)
        self.source_name = self.as_dict.get("source_name", None)
        self.tags = self.as_dict.get("tags", None)
        self.total_calls = self.as_dict.get("total_calls", None)
        self.value = self.as_dict.get("value", None)
        self.waveforms = self.as_dict.get("waveforms", None)
        self.tracker_id = self.as_dict.get("tracker_id", None)
        self.speaker_percent = self.as_dict.get("speaker_percent", None)
        self.keywords = self.as_dict.get("keywords", None)
        self.media = self.as_dict.get("media", None)
        self.campaign = self.as_dict.get("campaign", None)
        self.referring_url = self.as_dict.get("referring_url", None)
        self.landing_page_url = self.as_dict.get("landing_page_url", None)
        self.last_requested_url = self.as_dict.get("last_requested_url", None)
        self.referrer_domain = self.as_dict.get("referrer_domain", None)
        self.utm_source = self.as_dict.get("utm_source", None)
        self.utm_medium = self.as_dict.get("utm_medium", None)
        self.utm_term = self.as_dict.get("utm_term", None)
        self.utm_content = self.as_dict.get("utm_content", None)
        self.utm_campaign = self.as_dict.get("utm_campaign", None)
        self.utma = self.as_dict.get("utma", None)
        self.utmb = self.as_dict.get("utmb", None)
        self.utmc = self.as_dict.get("utmc", None)
        self.utmv = self.as_dict.get("utmv", None)
        self.utmz = self.as_dict.get("utmz", None)
        self.ga = self.as_dict.get("ga", None)
        self.gclid = self.as_dict.get("gclid", None)
        self.fbclid = self.as_dict.get("fbclid", None)
        self.msclkid = self.as_dict.get("msclkid", None)
        self.milestones = self.as_dict.get("milestones", None)
        self.timeline_url = self.as_dict.get("timeline_url", None)
        self.keywords_spotted = self.as_dict.get("keywords_spotted", None)
        self.call_highlights = self.as_dict.get("call_highlights", None)
        self.agent_email = self.as_dict.get("agent_email", None)
        self.keypad_entries = self.as_dict.get("keypad_entries", None)

    def update(
            self,
            update: dict):
        """Updates the current call object with the latest data from the API"""
        self.as_dict = self.parent.parent._put(
            endpoint = 'a',
            path = f'/{self.parent.id}/calls/{self.id}.json',
            data = update
        )
        self.__extract_from_data()
    
    def _refresh(self):
        """Refreshes the current call object with the latest data from the API"""
        self.as_dict: dict = self.parent.get_call(self.id, obj_or_dict='dict')
        self.__extract_from_data()

    def __repr__(self):
        return f'Call({self.id})'
    
    def __str__(self):
        return f'Call({self.id})'
    
    def __dict__(self):
        return self.as_dict