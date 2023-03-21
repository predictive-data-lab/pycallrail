from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, ClassVar
import datetime as dt
from enum import Enum

if TYPE_CHECKING:
    from ..callrail import *

from api.accounts import *

class Company:
    """
    A class representing a CallRail company.
    """
    parent: ClassVar[Account]

    id: str
    name: str   
    status: str
    time_zone: str
    created_at: dt.datetime
    disabled_at: Optional[dt.datetime]
    dni_active: Optional[bool]
    script_url: str
    callscore_enabled: bool
    lead_scoring_enabled: bool
    # deprecated
    swap_exclude_jquery: Optional[bool]
    swap_ppc_override: Optional[bool]
    swap_landing_override: Optional[bool]
    swap_cookie_duration: Optional[int]
    callscribe_enabled: Optional[bool]
    # deprecated
    keyword_spotting_enabled: Optional[bool]
    form_capture: Optional[bool]
    verrified_caller_ids: Optional[List[dict]]

    def __init__(self, data: Dict[str, Any], parent: Account):
        self.parent = parent
        if data is not None:
            self.as_dict = data
            self.__extract_from_data()
        
    def __extract_from_data(self):
        self.id = self.as_dict.get('id', None)
        self.name = self.as_dict.get('name', None)
        self.status = self.as_dict.get('status', None)
        self.time_zone = self.as_dict.get('time_zone', None)
        self.created_at = dt.datetime.fromisoformat(self.as_dict.get('created_at', None))
        self.disabled_at = dt.datetime.fromisoformat(self.as_dict.get('disabled_at', None)) if self.as_dict.get('disabled_at', None) else None
        self.dni_active = self.as_dict.get('dni_active', None)
        self.script_url = self.as_dict.get('script_url', None)
        self.callscore_enabled = self.as_dict.get('callscore_enabled', None)
        self.lead_scoring_enabled = self.as_dict.get('lead_scoring_enabled', None)
        self.swap_exclude_jquery = self.as_dict.get('swap_exclude_jquery', None)
        self.swap_ppc_override = self.as_dict.get('swap_ppc_override', None)
        self.swap_landing_override = self.as_dict.get('swap_landing_override', None)
        self.swap_cookie_duration = self.as_dict.get('swap_cookie_duration', None)
        self.callscribe_enabled = self.as_dict.get('callscribe_enabled', None)
        self.keyword_spotting_enabled = self.as_dict.get('keyword_spotting_enabled', None)
        self.form_capture = self.as_dict.get('form_capture', None)
        self.verrified_caller_ids = self.as_dict.get('verrified_caller_ids', None)

    def update(
            self,
            update_data: Dict[str, Any]
    ):
        """
        Update the company.
        """
        self.as_dict = self.parent.parent._put(
            endpoint = 'a',
            path = f'/{self.parent.id}/companies/{self.id}.json',
            data = update_data
        )
        self.__extract_from_data()

    def delete(self):
        """
        Delete the company.
        """
        self.parent.parent._delete(
            endpoint = 'a',
            path = f'/{self.parent.id}/companies/{self.id}.json'
        )
    
    def __repr__(self) -> str:
        return f"Company(id={self.id}, name={self.name}, status={self.status}, time_zone={self.time_zone}, created_at={self.created_at}, disabled_at={self.disabled_at}, dni_active={self.dni_active}, script_url={self.script_url}, callscore_enabled={self.callscore_enabled}, lead_scoring_enabled={self.lead_scoring_enabled}, swap_exclude_jquery={self.swap_exclude_jquery}, swap_ppc_override={self.swap_ppc_override}, swap_landing_override={self.swap_landing_override}, swap_cookie_duration={self.swap_cookie_duration}, callscribe_enabled={self.callscribe_enabled}, keyword_spotting_enabled={self.keyword_spotting_enabled}, form_capture={self.form_capture}, verrified_caller_ids={self.verrified_caller_ids})"
    
    def __str__(self) -> str:
        return f"Company(id={self.id}, name={self.name}, status={self.status}, time_zone={self.time_zone}, created_at={self.created_at}, disabled_at={self.disabled_at}, dni_active={self.dni_active}, script_url={self.script_url}, callscore_enabled={self.callscore_enabled}, lead_scoring_enabled={self.lead_scoring_enabled}, swap_exclude_jquery={self.swap_exclude_jquery}, swap_ppc_override={self.swap_ppc_override}, swap_landing_override={self.swap_landing_override}, swap_cookie_duration={self.swap_cookie_duration}, callscribe_enabled={self.callscribe_enabled}, keyword_spotting_enabled={self.keyword_spotting_enabled}, form_capture={self.form_capture}, verrified_caller_ids={self.verrified_caller_ids})"
    
    def __dict__(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "time_zone": self.time_zone,
            "created_at": self.created_at,
            "disabled_at": self.disabled_at,
            "dni_active": self.dni_active,
            "script_url": self.script_url,
            "callscore_enabled": self.callscore_enabled,
            "lead_scoring_enabled": self.lead_scoring_enabled,
            "swap_exclude_jquery": self.swap_exclude_jquery,
            "swap_ppc_override": self.swap_ppc_override,
            "swap_landing_override": self.swap_landing_override,
            "swap_cookie_duration": self.swap_cookie_duration,
            "callscribe_enabled": self.callscribe_enabled,
            "keyword_spotting_enabled": self.keyword_spotting_enabled,
            "form_capture": self.form_capture,
            "verrified_caller_ids": self.verrified_caller_ids
        }
    
