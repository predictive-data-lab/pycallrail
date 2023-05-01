from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING, ClassVar, cast
import datetime as dt
from enum import Enum

if TYPE_CHECKING:
    from pycallrail.callrail import *

from pycallrail.api.accounts import *
from pycallrail.api.companies import *

class Tracker:
    """
    Trackers are phone numbers that can be used to route phone calls to a business. 
    CallRail provides two different types of trackers.

    See more at: https://apidocs.callrail.com/#trackers
    """

    parent: Account

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

    def __init__(self, parent: Account, data: Dict[str, Any]) -> None:
        self.parent = parent
        self.as_dict: Dict[str, Union[str, bool]] = data
        self.__extract_from_data()
        
    def __extract_from_data(self) -> None:
        self.id = cast(str,self.as_dict.get('id'))
        self.name = cast(str,self.as_dict.get('name'))
        self.type = cast(str,self.as_dict.get('type'))
        self.destination_number = cast(str,self.as_dict.get('destination_number'))
        self.status = cast(str,self.as_dict.get('status'))
        self.tracking_number = cast(str,self.as_dict.get('tracking_number'))
        self.whisper_message = cast(str,self.as_dict.get('whisper_message'))
        self.sms_enabled = bool(self.as_dict.get('sms_enabled'))
        self.sms_supported = bool(self.as_dict.get('sms_supported'))
        self.company = Company(parent = self.parent, data = cast(dict,self.as_dict.get('company')))
        self.call_flow = cast(dict,self.as_dict.get('call_flow'))
        self.source = cast(Dict[str, List[str]],self.as_dict.get('source'))
        self.created_at = dt.datetime.fromisoformat(cast(str,self.as_dict.get('created_at')))
        self.disabled_at = dt.datetime.fromisoformat(cast(Optional[str], self.as_dict.get('disabled_at'))) if self.as_dict.get('disabled_at') else None # type: ignore
        self.campaign_name = cast(Optional[str],self.as_dict.get('campaign_name', None))
        self.swap_targets = cast(Optional[List[str]], self.as_dict.get('swap_targets', None))

    def disable(self) -> None:
        """
        Disable a tracker.
        """
        if self.status == 'disabled':
            logging.warning(f'Tracker {self.id} is already disabled')
            
        
        else:
            self.parent.parent._delete(f'/v3/a/{self.parent.id}/trackers/{self.id}')
            self.status = 'disabled'


