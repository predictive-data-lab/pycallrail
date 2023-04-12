from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING, ClassVar
import datetime as dt
from enum import Enum

if TYPE_CHECKING:
    from pycallrail.callrail import *

from pycallrail.api.accounts import Account
from pycallrail.api.companies import Company

class Tracker:
    """
    Trackers are phone numbers that can be used to route phone calls to a business. 
    CallRail provides two different types of trackers.

    See more at: https://apidocs.callrail.com/#trackers
    """

    parent: ClassVar[Account]

    id: str
    name: str
    type: str
    destination_number: str
    status: str 
    tracking_number: str
    whisper_message: str
    sms_enabled: bool
    sms_supported: bool
    company: Company
    call_flow: Dict[str, Any]
    source: Dict[str, List[str]]
    created_at: dt.datetime
    disabled_at: Optional[dt.datetime]
    campaign_name: Optional[str]
    swap_targets: Optional[List[str]]

    def __init__(self, parent: Account, data: Dict[str, Any]):
        self.parent = parent
        if data is not None:
            self.as_dict = data
            self.__extract_from_data()
        else:
            raise ValueError('Did you really try to create a Tracker with no data?')
        
    def __extract_from_data(self) -> None:
        self.id = self.as_dict.get('id')
        self.name = self.as_dict.get('name')
        self.type = self.as_dict.get('type')
        self.destination_number = self.as_dict.get('destination_number')
        self.status = self.as_dict.get('status')
        self.tracking_number = self.as_dict.get('tracking_number')
        self.whisper_message = self.as_dict.get('whisper_message')
        self.sms_enabled = self.as_dict.get('sms_enabled')
        self.sms_supported = self.as_dict.get('sms_supported')
        self.company = Company(self.parent, self.as_dict.get('company'))
        self.call_flow = self.as_dict.get('call_flow')
        self.source = self.as_dict.get('source')
        self.created_at = dt.datetime.fromisoformat(self.as_dict.get('created_at'))
        self.disabled_at = dt.datetime.fromisoformat(self.as_dict.get('disabled_at')) if self.as_dict.get('disabled_at') else None
        self.campaign_name = self.as_dict.get('campaign_name') or None
        self.swap_targets = self.as_dict.get('swap_targets') or None

    def disable(self) -> None:
        """
        Disable a tracker.
        """
        self.parent.parent._delete(f'/v3/a/{self.parent.id}/trackers/{self.id}')
        self.status = 'disabled'

