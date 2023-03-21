from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING, ClassVar
import datetime as dt
from enum import Enum

if TYPE_CHECKING:
    from ..callrail import *

from api.accounts import *

class FormSubmission:
    """
    Represents a Form Submission in CallRail.
    """
    parent: ClassVar[Account]

    id: str
    company_id: str
    person_id: str
    form_data: Dict[str, Any]
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
    keywords: Optional[str]
    campaign: Optional[str]
    medium: Optional[str]

    # user requested fields
    lead_status: Optional[str]
    value: float | int
    note: Optional[str]
    tags: List[str]
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    form_name: Optional[str]
    timeline_url: Optional[str]

    def __init__(self, parent: Account, data: Dict[str, Any]):
        self.parent = parent
        if data is not None:
            self.as_dict = data
            self.__extract_from_data()

    def __extract_from_data(self):
        self.id = self.as_dict.get('id', None)
        self.company_id = self.as_dict.get('company_id', None)
        self.person_id = self.as_dict.get('person_id', None)
        self.form_data = self.as_dict.get('form_data', None)
        self.form_url = self.as_dict.get('form_url', None)
        self.landing_page_url = self.as_dict.get('landing_page_url', None)
        self.referrer = self.as_dict.get('referrer', None)
        self.referring_url = self.as_dict.get('referring_url', None)
        self.submitted_at = dt.datetime.fromisoformat(self.as_dict.get('submitted_at', None))
        self.first_form = self.as_dict.get('first_form', None)
        self.customer_phone_number = self.as_dict.get('customer_phone_number', None)
        self.customer_name = self.as_dict.get('customer_name', None)
        self.formatted_customer_phone_number = self.as_dict.get('formatted_customer_phone_number', None)
        self.formatted_customer_name = self.as_dict.get('formatted_customer_name', None)
        self.source = self.as_dict.get('source', None)
        self.keywords = self.as_dict.get('keywords', None)
        self.campaign = self.as_dict.get('campaign', None)
        self.medium = self.as_dict.get('medium', None)

        # user requested fields
        self.lead_status = self.as_dict.get('lead_status', None)
        self.value = self.as_dict.get('value', None)
        self.note = self.as_dict.get('note', None)
        self.tags = self.as_dict.get('tags', None)
        self.utm_source = self.as_dict.get('utm_source', None)
        self.utm_medium = self.as_dict.get('utm_medium', None)
        self.utm_campaign = self.as_dict.get('utm_campaign', None)
        self.form_name = self.as_dict.get('form_name', None)
        self.timeline_url = self.as_dict.get('timeline_url', None)

    def update(
            self,
            update_data: Dict[str, Any]
    ) -> None:
        """
        Update a form submission in CallRail.
        """
        self.as_dict = self.parent.parent._put(
            endpoint = 'a',
            path = f'/{self.parent.id}/form_submissions/{self.id}.json',
            data = update_data
        )
        self.__extract_from_data()

    