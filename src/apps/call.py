# internal
from src import sheet
from src import settings
from .base import BaseApp
from src import connection
# external
from jdatetime import date


class CallModel(object):
    """Call Model"""
    def __init__(self, connection, n, call_id, action):
        self.connection = connection
        self.n = n
        self.action = action
        self.call_id = call_id
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
        # check for full initialize
        if action != 3:
            self._init()

    def _init(self):
        sql = """
            SELECT *
            FROM viwCallHistory
            WHERE ID = ?
        """
        query = self.connection.execute(sql, [self.call_id])
        if not query.next():
            raise Exception('Call {} does not exists'.format(self.call_id))
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
            self.call_id,
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

    def done(self):
        sql = "DELETE FROM MGS WHERE n = ? AND id = ?"
        query = self.connection.execute(sql, [self.n, self.call_id])
        query.clear()
        return True


class CallApp(BaseApp):
    """Call History App"""
    def __init__(self, interval):
        super().__init__(interval)
        self._sheet = None
        self.connection = connection.get('app')
        self.blacklist = settings.g('call_blacklist')

    @property
    def sheet(self):
        if self._sheet is None:
            self._sheet = sheet.get(settings.g('call_sheet'))
        return self._sheet

    def get_calls(self):
        sql = "SELECT n, id, act FROM MGS WHERE subject = 3 ORDER BY n"
        query = self.connection.execute(sql)
        calls = list()
        while query.next():
            calls.append(CallModel(self.connection, query.value(0), query.value(1), query.value(2)))
        query.clear()
        return calls

    def _do(self):
        inserted = 0
        updated = 0
        deleted = 0
        report = list()
        today = date.today().strftime('%Y/%m/%d')
        for call in self.get_calls():
            # find cell
            cell = self.sheet.find(str(call.call_id), in_column=1)
            if call.date != today or call.number in self.blacklist:
                # do nothing untill call.done()
                pass
            elif call.action == 1:
                self.sheet.append_row(call.serialize())
                inserted += 1
            elif call.action == 2:
                if cell:
                    self.sheet.update('A{}:L{}'.format(cell.row, cell.row), [call.serialize()])
                    updated += 1
                else:
                    self.sheet.append_row(call.serialize())
                    inserted += 1
            else:
                if cell:
                    self.sheet.delete_row(cell.row)
                    deleted += 1
            call.done()
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
