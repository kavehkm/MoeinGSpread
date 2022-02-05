# standard
from time import time
# internal
from src import sheet
from src import connection as conn


class BaseModel(object):
    """Base Model"""
    def __init__(self, connection, n, model_id, action):
        self.connection = connection
        self.n = n
        self.model_id = model_id
        self.action = action
        if action != 3:
            self._init()

    def _init(self):
        pass

    @property
    def pk(self):
        return self.model_id

    def serialize(self):
        return [
            self.model_id
        ]

    def done(self):
        sql = "DELETE FROM MGS WHERE n = ? AND id = ?"
        query = self.connection.execute(sql, [self.n, self.model_id])
        query.clear()
        return True


class BaseApp(object):
    """Base Application"""
    SUBJECT = 0
    NAME = 'BaseApp'
    MODEL = BaseModel

    def __init__(self, interval, sheet_names=()):
        self._ran = 0
        self._interval = interval
        self._sheet_names = sheet_names
        self.connection = conn.get('app')
        self._sheets = None

    @property
    def sheets(self):
        if self._sheets is None:
            self._sheets = [sheet.get(name) for name in self._sheet_names]
        return self._sheets

    def sheets_append(self, values):
        for sh in self.sheets:
            sh.append_row(values)

    def sheets_delete(self, pk):
        for sh in self.sheets:
            cell = sh.find(str(pk), in_column=1)
            if cell:
                sh.delete_row(cell.row)

    def sheets_update(self, pk, values):
        for sh in self.sheets:
            cell = sh.find(str(pk), in_column=1)
            if cell:
                sh.delete_row(cell.row)
                sh.insert_row(values, cell.row)
            else:
                sh.append_row(values)

    def get_objects(self):
        sql = "SELECT n, id, act FROM MGS WHERE subject = ? ORDER BY n"
        query = self.connection.execute(sql, [self.SUBJECT])
        objects = list()
        while query.next():
            n = query.value(0)
            model_id = query.value(1)
            action = query.value(2)
            objects.append(self.MODEL(self.connection, n, model_id, action))
        query.clear()
        return objects

    def _do(self):
        inserted = 0
        updated = 0
        deleted = 0
        report = list()

        for obj in self.get_objects():
            if obj.action == 1:
                self.sheets_append(obj.serialize())
                inserted += 1
            elif obj.action == 2:
                self.sheets_update(obj.pk, obj.serialize())
                updated += 1
            else:
                self.sheets_delete(obj.pk)
                deleted += 1
            obj.done()
        # generate report
        if inserted:
            report.append('{} new {} inserted'.format(inserted, self.NAME.lower()))
        if updated:
            report.append('{} {} updated'.format(updated, self.NAME.lower()))
        if deleted:
            report.append('{} {} deleted'.format(deleted, self.NAME.lower()))
        if report:
            return {
                'title': self.NAME.title(),
                'message': '\n'.join(report)
            }

    def run(self):
        # check for period
        if time() - self._ran > self._interval:
            result = self._do()
            # save ran time
            self._ran = time()
            return result
