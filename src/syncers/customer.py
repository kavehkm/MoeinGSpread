# internal
from src import settings
from .base import BaseSyncer
from src.utils import split_tels
from src.models import Customer, MGS


class Customer(BaseSyncer):
    """Customer Syncer"""

    MODEL = Customer
    TARGETS = settings.g('customer_sheet')
    SUBJECT = MGS.CUSTOMER

    def serialize(self, instance):
        record = [
            instance.id,
            instance.code,
            instance.name,
            instance.email,
            instance.state,
            instance.city,
            instance.address,
            instance.post_code,
            instance.company,
            instance.company_address,
            instance.info,
            instance.group_name
        ]
        for tel in split_tels(instance.tels):
            record.append(tel)
        return record
