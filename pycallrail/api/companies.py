from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, ClassVar, get_type_hints
import datetime as dt
from enum import Enum

from . import accounts

class Company:
    """
    A class representing a CallRail company.
    """
    parent: accounts.Account

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
    verified_caller_ids: Optional[List[dict]]

    _REQUIRED_FIELDS: ClassVar[List[str]] = [
        'id',
        'name',
        'status',
        'time_zone',
        'created_at',
    ]
    def __init__(self, data: Optional[dict], parent: accounts.Account):
        
        
        if not isinstance(parent, accounts.Account):
            raise TypeError("parent must be an instance of Account")
        
        if data is None:
            raise ValueError("data must not be None")
        
        

        self.parent = parent
        self.as_dict = data
        self.__extract_from_data()
        
    def __extract_from_data(self):
        self.id = self.as_dict.get('id', None) # type: ignore
        self.name = self.as_dict.get('name', None) # type: ignore
        self.status = self.as_dict.get('status', None) # type: ignore
        self.time_zone = self.as_dict.get('time_zone', None) # type: ignore
        self.created_at = dt.datetime.fromisoformat(self.as_dict.get('created_at')) if self.as_dict.get('created_at', None) else None # type: ignore
        self.disabled_at = dt.datetime.fromisoformat(self.as_dict.get('disabled_at')) if self.as_dict.get('disabled_at', None) else None # type: ignore
        self.dni_active = self.as_dict.get('dni_active', None) # type: ignore
        self.script_url = self.as_dict.get('script_url', None) # type: ignore
        self.callscore_enabled = self.as_dict.get('callscore_enabled', None) # type: ignore
        self.lead_scoring_enabled = self.as_dict.get('lead_scoring_enabled', None) # type: ignore
        self.swap_exclude_jquery = self.as_dict.get('swap_exclude_jquery', None) # type: ignore
        self.swap_ppc_override = self.as_dict.get('swap_ppc_override', None) # type: ignore
        self.swap_landing_override = self.as_dict.get('swap_landing_override', None) # type: ignore
        self.swap_cookie_duration = self.as_dict.get('swap_cookie_duration', None) # type: ignore
        self.callscribe_enabled = self.as_dict.get('callscribe_enabled', None) # type: ignore
        self.keyword_spotting_enabled = self.as_dict.get('keyword_spotting_enabled', None) # type: ignore
        self.form_capture = self.as_dict.get('form_capture', None) # type: ignore
        self.verified_caller_ids = self.as_dict.get('verified_caller_ids', None) # type: ignore

    def update(
            self,
            update_data: Dict[str, Any]
    ):
        """
        Update the company.
        """
        if update_data is None:
            raise ValueError("update_data must not be None")
        
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
        return f"Company(id={self.id}, name={self.name}, status={self.status}, time_zone={self.time_zone}, created_at={self.created_at}, disabled_at={self.disabled_at}, dni_active={self.dni_active}, script_url={self.script_url}, callscore_enabled={self.callscore_enabled}, lead_scoring_enabled={self.lead_scoring_enabled}, swap_exclude_jquery={self.swap_exclude_jquery}, swap_ppc_override={self.swap_ppc_override}, swap_landing_override={self.swap_landing_override}, swap_cookie_duration={self.swap_cookie_duration}, callscribe_enabled={self.callscribe_enabled}, keyword_spotting_enabled={self.keyword_spotting_enabled}, form_capture={self.form_capture}, verrified_caller_ids={self.verified_caller_ids})"
    
    def __str__(self) -> str:
        return f"Company(id={self.id}, name={self.name}, status={self.status}, time_zone={self.time_zone}, created_at={self.created_at}, disabled_at={self.disabled_at}, dni_active={self.dni_active}, script_url={self.script_url}, callscore_enabled={self.callscore_enabled}, lead_scoring_enabled={self.lead_scoring_enabled}, swap_exclude_jquery={self.swap_exclude_jquery}, swap_ppc_override={self.swap_ppc_override}, swap_landing_override={self.swap_landing_override}, swap_cookie_duration={self.swap_cookie_duration}, callscribe_enabled={self.callscribe_enabled}, keyword_spotting_enabled={self.keyword_spotting_enabled}, form_capture={self.form_capture}, verrified_caller_ids={self.verified_caller_ids})"
    
    def __dict__(self) -> Dict[str, Any]: # type: ignore
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
            "verrified_caller_ids": self.verified_caller_ids
        }
    
