# internal
from src import settings
from .base import BaseSyncer
from src.models import Call, MGS

# jdatetime
from jdatetime import date


class Call(BaseSyncer):
    """Call Syncer"""

    MODEL = Call
    SUBJECT = MGS.CALL
    TRACKER = settings.g('call_tracker')
    TARGETS = settings.g('call_targets', [])

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
    
    def pass_log(self, log):
        if log.act == MGS.DELETE:
            return False
        call = self.MODEL.get(log.id)
        today = date.today().strftime('%Y/%m/%d')
        if call.date != today or call.number in settings.g('call_blacklist'):
            return True
        return False
