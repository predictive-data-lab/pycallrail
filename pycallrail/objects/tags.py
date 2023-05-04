from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pycallrail.base as base
import pycallrail.callrail as crl
import typing
import logging
import typeguard

@typeguard.typechecked
class Tag(base.CallRailBase):
    """
    Represents a Tag.

    More information: https://apidocs.callrail.com/#tags
    """

    id: typing.Union[int, str]
    name: str
    tag_level: str
    color: str
    background_color: str
    company_id: str
    status: str
    created_at: dt.datetime

    def __init__(
        self,
        api_client: crl.CallRail,
        account_id: str,
        id: typing.Union[int, str],
        name: str,
        tag_level: str,
        color: str,
        background_color: str,
        company_id: str,
        status: str,
        created_at: dt.datetime
    ) -> None:
        super(Tag, self).__init__()
        self.api_client: crl.CallRail = api_client
        self.account_id = account_id
        self.id = id
        self.name = name    
        self.tag_level = tag_level
        self.color = color
        self.background_color = background_color
        self.company_id = company_id
        self.status = status
        self.created_at = created_at

    @classmethod
    def from_json(
        cls,
        api_client: crl.CallRail,
        account_id: str,
        json_data: typing.Dict[str, typing.Any]
    ) -> Tag:
        """
        Deserialize JSON data to a Tag object.
        """
        json_data['created_at'] = dateparser.parse(json_data['created_at'])

        return cls(
            api_client=api_client,
            account_id=account_id,
            id=json_data['id'],
            name=json_data['name'],
            tag_level=json_data['tag_level'],
            color=json_data['color'],
            background_color=json_data['background_color'],
            company_id=json_data['company_id'],
            status=json_data['status'],
            created_at=json_data['created_at']
        )
    
    def update(
            self,
            name: typing.Optional[str] = None,
            color: typing.Optional[str] = None,
            disabled: typing.Optional[typing.Union[str, bool]] = None
    ) -> None:
        """
        Updates the Tag.
        """
        if name:
            self.name = name
        if color:
            self.color = color
        if disabled == 'true' or disabled == True:
            self.disabled = True

        body: typing.Dict[str, typing.Any] = {
            'name': name,
            'color': color,
            'disabled': disabled
        }

        response: typing.Dict[str, typing.Any] = typing.cast(
            typing.Dict[str, typing.Any],
            self.api_client._put(
                endpoint=f'a/{self.account_id}',
                path=f'tags/{self.id}.json',
                data=body
            )
        )

        for key, value in response.items():
            if key not in self.__class__.__annotations__.keys():
                raise AttributeError(f'{key} is not a valid attribute for {self.__class__.__name__}')
            else:
                setattr(self, key, value)
    
    def delete(self) -> None:
        """
        Deletes the Tag.
        """
        self.api_client._delete(
            endpoint=f'a/{self.account_id}',
            path=f'tags/{self.id}.json'
        )

    