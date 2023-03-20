from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
import logging
import datetime as dt

if TYPE_CHECKING:
    from ..callrail import *

class Account:
    """
    Represents an account in CallRail
    """
    
    id: str
    name: str
    outbound_recording_enabled: bool
    hipaa_account: bool
    numeric_id: Optional[int]

    def __init__(
            self,
            data: Optional[dict],
            parent: CallRail)
        self.parent = parent
        if data is not None:
            self.as_dict = data
            self.__extract_from_data()

    def __extract_from_data(self):
        self.id = self.as_dict.get("id")
        self.name = self.as_dict.get("name")
        self.outbound_recording_enabled = self.as_dict.get("outbound_recording_enabled")
        self.hipaa_account = self.as_dict.get("hipaa_account")
        if self.as_dict.get("numeric_id"):
            self.numeric_id = self.as_dict.get("numeric_id")

    def __dict__(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "outbound_recording_enabled": self.outbound_recording_enabled,
            "hipaa_account": self.hipaa_account,
            "numeric_id": self.numeric_id,
        }
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"Account: {self.name}"