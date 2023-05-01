from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, ClassVar, cast, Iterable
import logging
import datetime as dt
from enum import Enum

if TYPE_CHECKING:
    from ..callrail import *

from pycallrail.api.accounts import *
import jsonschema


class Tag:
    """
    Tag object.
    """
    parent: Account

    id: str
    name: str
    tag_level: str
    color: str
    background_color: str
    company_id: str
    status: str
    created_at: Optional[dt.datetime]

    _tag_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "id": {"anyOf": [
                {'type': 'string'},
                {'type': 'integer'}
            ]},
            "name": {"type": "string"},
            "tag_level": {"type": "string"},
            "color": {"type": "string"},
            "background_color": {"type": "string"},
            "company_id": {"type": "string"},
            "status": {"type": "string"},
            "created_at": {"type": "string"}
        },
        "required": [
            "id",
            "name",
            "tag_level",
            "color"
        ]
    }
    def __init__(self, data: dict[str, Any], parent: Account) -> None:
        
        self.parent = parent

        self._validate_data(data)

        
        if data is None:
            raise ValueError('data cannot be None')

        self.as_dict: dict[str, Any] = data
        self.__extract_from_data()
        
    def __extract_from_data(self, all: bool = True, keys: Optional[Iterable[str]] = None) -> None:
        
        if all:
            self.id = str(self.as_dict.get('id')) 
            self.name = self.as_dict.get('name', None)
            self.tag_level = self.as_dict.get('tag_level', None)
            self.color = self.as_dict.get('color', None)
            self.background_color = self.as_dict.get('background_color', None)
            self.company_id = self.as_dict.get('company_id', None)
            self.status = self.as_dict.get('status', None)
            self.created_at = dt.datetime.fromisoformat(cast(str,self.as_dict.get('created_at'))) if self.as_dict.get('created_at') else None
        else:
            if keys is None:
                raise ValueError('keys cannot be None when not updating all attributes')
            # update only the keys specified
            for key in cast(list[str], keys):
                setattr(self, key, self.as_dict.get(key, None))

    def update(
            self,
            update_data: dict[str, Any],
            keys: Optional[Iterable[str]] = None,
            all: bool = True
    ) -> None:
        """
        Update a tag.
        """
        self._validate_data(update_data)
        
        self.as_dict = cast(dict[str, Any], self.parent.parent._put(
            endpoint = 'a',
            path = f'/{self.parent.id}/tags/{self.id}.json',
            data = update_data
        ))
        self.__extract_from_data(all=all, keys=keys)

    def delete(
            self,
    ) -> None:
        """
        Delete a tag.
        """
        self.parent.parent._delete(
            endpoint = 'a',
            path = f'/{self.parent.id}/tags/{self.id}.json'
        )

    def __dict__(self) -> dict[str, Any]: # type: ignore
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
    
    def _validate_data(self, data) -> None:
        try:
            jsonschema.validate(instance=data, schema=self._tag_schema)
        except jsonschema.ValidationError as e:
            raise TypeError(f'Invalid data: {e}') from e