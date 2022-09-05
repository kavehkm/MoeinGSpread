# internal
from src import settings
from .base import BaseSyncer
from src.utils import split_tels
from src.models import Invoice, MGS


class Invoice(BaseSyncer):
    """Invoice Syncer"""

    MODEL = Invoice
    SUBJECT = MGS.INVOICE
    TRACKER = settings.g('invoice_tracker')
    TARGETS = settings.g('invoice_targets', [])

    def serialize(self, instance):
        record = [
            instance.id,
            instance.fish_no,
            instance.date,
            instance.time,
            instance.address,
            instance.code,
            instance.name,
            instance.send_time,
            instance.info,
            instance.total,
            '\n'.join(['{name} * {quantity}'.format(**item) for item in instance.items])
        ]
        for tel in split_tels(instance.tel):
            record.append(tel)
        return record
