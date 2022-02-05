# internal
from .base import BaseApp, BaseModel
# external
from jdatetime import date


class CallModel(BaseModel):
    """Call Model"""
    def __init__(self, *args, **kwargs):
        self.date = None
        self.time = None
        self.line = None
        self.number = None
        self.user_id = None
        self.accept = None
        self.customer_id = None
        self.code = None
        self.name = None
        self.address = None
        self.username = None
        super().__init__(*args, **kwargs)

    def _init(self):
        sql = """
            SELECT *
            FROM viwCallHistory
            WHERE ID = ?
        """
        query = self.connection.execute(sql, [self.model_id])
        if not query.next():
            raise Exception('Call {} does not exists'.format(self.model_id))
        # initialization
        self.date = query.value(1)
        self.time = query.value(2)
        self.line = query.value(3)
        self.number = query.value(4)
        self.user_id = query.value(5)
        self.accept = query.value(6)
        self.customer_id = query.value(7)
        self.code = query.value(8)
        self.name = query.value(10)
        self.address = query.value(11)
        self.username = query.value(12)
        query.clear()

    def serialize(self):
        return [
            self.model_id,
            self.date,
            self.time,
            self.line,
            self.number,
            self.accept,
            self.customer_id,
            self.code,
            self.name,
            self.address,
            self.user_id,
            self.username
        ]


class CallApp(BaseApp):
    """Call History App"""
    SUBJECT = 3
    NAME = 'Call'
    MODEL = CallModel

    def __init__(self, *args, **kwargs):
        self.blacklist = kwargs.pop('blacklist', [])
        super().__init__(*args, **kwargs)

    def _do(self):
        inserted = 0
        updated = 0
        deleted = 0
        report = list()
        today = date.today().strftime('%Y/%m/%d')

        for call in self.get_objects():
            if call.date != today or call.number in self.blacklist:
                # do nothing untill call.done()
                pass
            elif call.action == 1:
                self.sheets_append(call.serialize())
                inserted += 1
            elif call.action == 2:
                self.sheets_update(call.pk, call.serialize())
                updated += 1
            else:
                self.sheets_delete(call.pk)
                deleted += 1
            call.done()
        # generate report
        if inserted:
            report.append('{} new call inserted'.format(inserted))
        if updated:
            report.append('{} call updated'.format(updated))
        if deleted:
            report.append('{} call deleted'.format(deleted))
        if report:
            return {
                'title': 'Call',
                'message': '\n'.join(report)
            }
