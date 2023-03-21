from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, ClassVar
import logging
import datetime as dt
from enum import Enum

if TYPE_CHECKING:
    from ..callrail import *

from api.accounts import *

class Tag:
    """
    Tag object.
    """
    parent: ClassVar[Account]

    id: str
    name: str
    tag_level: str
    color: str
    background_color: str
    company_id: str
    status: str
    created_at: dt.datetime

    def __init__(self, data: Dict[str, Any], parent: Account):
        self.parent = parent
        if data is not None:
            self.as_dict = data
            self.__extract_from_data()
        
    def __extract_from_data(self):
        self.id = self.as_dict.get('id', None)
        self.name = self.as_dict.get('name', None)
        self.tag_level = self.as_dict.get('tag_level', None)
        self.color = self.as_dict.get('color', None)
        self.background_color = self.as_dict.get('background_color', None)
        self.company_id = self.as_dict.get('company_id', None)
        self.status = self.as_dict.get('status', None)
        self.created_at = dt.datetime.fromisoformat(self.as_dict.get('created_at', None))

    def update(
            self,
            update_data: Dict[str, Any]
    ):
        """
        Update a tag.
        """
        self.as_dict = self.parent.parent._put(
            endpoint = 'a',
            path = f'/{self.parent.id}/tags/{self.id}.json',
            data = update_data
        )
        self.__extract_from_data()

    def delete(
            self,
    ):
        """
        Delete a tag.
        """
        self.parent.parent._delete(
            endpoint = 'a',
            path = f'/{self.parent.id}/tags/{self.id}.json'
        )

    def __dict__(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "tag_level": self.tag_level,
            "color": self.color,
            "background_color": self.background_color,
            "company_id": self.company_id,
            "status": self.status,
            "created_at": self.created_at
        }
    