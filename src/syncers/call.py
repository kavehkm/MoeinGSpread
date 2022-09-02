# internal
from src import settings
from .base import BaseSyncer
from src.models import Call, MGS


class Call(BaseSyncer):
    """Call Syncer"""

    MODEL = Call
    SUBJECT = MGS.CALL
    TARGETS = settings.g('call_sheet', [])

    def serialize(self, instance):
        return [
            instance.id,
            instance.date,
            instance.time,
            instance.line,
            instance.number,
            instance.accept,
            instance.customer_id,
            instance.customer_code,
            instance.customer_name,
            instance.customer_address,
            instance.user_id,
            instance.user_name
        ]
