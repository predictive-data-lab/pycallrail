from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pycallrail.base as base
import pycallrail.callrail as crl
import typing
import typing_extensions
import requests


class FormSubmission(base.CallRailBase):
    """
    Represents a form submission.

    More info: https://apidocs.callrail.com/#form-submissions
    """

    # These fields are always returned by the API
    id: str
    company_id: str
    person_id: str
    form_data: typing.Dict[str, typing.Any]
    form_url: str
    landing_page_url: str
    referrer: str
    referring_url: str
    submitted_at: dt.datetime
    first_form: bool
    customer_phone_number: str
    customer_name: str
    formatted_customer_phone_number: str
    formatted_customer_name: str
    source: str
    keywords: str
    campaign: str
    medium: str

    # User Requested Fields
    lead_status: typing.Optional[str]
    value: typing.Optional[typing.Union[int, float]]
    note: typing.Optional[str]
    tags: typing.Optional[typing.List[typing.Any]]
    utm_source: typing.Optional[str]
    utm_campaign: typing.Optional[str]
    form_name: typing.Optional[str]
    timeline_url: typing.Optional[str]
    milestones: typing.Optional[typing.Any]

    def __init__(
        self,
        api_client: crl.CallRail,
        account_id: str,
        **kwargs
    ) -> None:
        super(FormSubmission, self).__init__()
        self.api_client: crl.CallRail = api_client
        self.account_id: str = account_id

        for k,v in kwargs.items():
            if k not in self.__class__.__annotations__.keys():
                raise AttributeError(f'{k} is not a valid attribute for {self.__class__.__name__}')
            else:
                setattr(self, k, v)

    @classmethod
    def from_json(
        cls,
        api_client: crl.CallRail,
        account_id: str,
        json_data: typing.Dict[str, typing.Any]
    ) -> FormSubmission:
        """
        Deserializes a FormSubmission from JSON.

        :param api_client: The CallRail API client
        :param json_data: The JSON data to deserialize
        :param account_id: The CallRail account ID
        :return: The FormSubmission object
        """
        json_data['submitted_at'] = dateparser.parse(json_data['submitted_at'])
        
        return cls(
            api_client=api_client,
            account_id=account_id,
            **json_data
        )
        
    def update(
        self,
        tags: typing.Optional[typing.List[typing.Any]] = None,
        note: typing.Optional[str] = None,
        value: typing.Optional[typing.Union[int, float]] = None,
        lead_status: typing.Optional[str] = None,
        append_tags: typing.Optional[bool] = None
    ) -> None:
        """
        Update a Form Submission.
        More information: https://apidocs.callrail.com/#updating-a-form-submission
        """

        # update the attributes
        if append_tags and tags and hasattr(self, 'tags'):
            self.tags.extend(tags) # type: ignore
        elif tags:
            self.tags = tags
        if note:
            self.note = note
        if value:
            self.value = value
        if lead_status:
            self.lead_status = lead_status

        # form the request
        body: typing.Dict[str, typing.Any] = {
            'tags': tags,
            'note': note,
            'value': value,
            'lead_status': lead_status
        }

        # send the request
        response: typing.Dict[str, typing.Any] = typing.cast(
            typing.Dict[str, typing.Any],
            self.api_client._put(
                endpoint=f'a/{self.account_id}',
                path=f'form_submissions/{self.id}.json',
                data=body
            )
        )

        # update the object
        for k,v in response.items():
            # raise an error if the attribute is not found
            if k not in self.__class__.__annotations__.keys():
                raise AttributeError(f'{k} is not a valid attribute for {self.__class__.__name__}')
            else:
                setattr(self, k, v)

        