# internal
from src import sheet
from src import settings
from .base import BaseApp
from src import connection


class InvoiceModel(object):
    """Invoice Model"""
    def __init__(self, connection, n, invoice_id, action):
        self.connection = connection
        self.n = n
        self.action = action
        self.invoice_id = invoice_id
        self.fishno = None
        self.date = None
        self.time = None
        self.tel = None
        self.address = None
        self.name = None
        self.send_time = None
        self.info = None
        self.total = None
        self.items = list()
        # check for full initialize
        if action != 3:
            self._init()

    def _init(self):
        sql = """
            SELECT f.FishNo, f.Date, f.Time, f.Tel, f.Address, f.MiddleMan,
            f.SendTime, f.Info, f.JamKol, a.Name, a.Tel, a.Address
            FROM Factor1 AS f
            INNER JOIN AshkhasList AS a ON f.IDShakhs = a.ID
            WHERE f.ID = ? 
        """
        query = self.connection.execute(sql, [self.invoice_id])
        if not query.next():
            raise Exception('Invoice {} does not exists'.format(self.invoice_id))
        # initialization
        self.fishno = query.value(0)
        self.date = query.value(1)
        self.time = query.value(2)
        self.tel = query.value(3) or query.value(10)
        self.address = query.value(4) or query.value(11)
        self.name = query.value(5) or query.value(9)
        self.send_time = query.value(6)
        self.info = query.value(7)
        self.total = query.value(8)
        query.clear()
        # find invoice items
        sql = """
            SELECT k.Name, f.Tedad
            FROM Faktor2 AS f
            INNER JOIN KalaList AS k ON k.ID = f.IDKala
            WHERE f.FactorID = ?
        """
        query = self.connection.execute(sql, [self.invoice_id])
        while query.next():
            self.items.append([query.value(0), int(query.value(1))])
        query.clear()

    def serialize(self):
        return [
            self.invoice_id,
            self.fishno,
            self.date,
            self.time,
            self.tel,
            self.address,
            self.name,
            self.send_time,
            self.info,
            self.total,
            '\n'.join(['{} * {}'.format(*item) for item in self.items])
        ]

    def done(self):
        sql = "DELETE FROM MGS WHERE n = ? AND id = ?"
        query = self.connection.execute(sql, [self.n, self.invoice_id])
        query.clear()
        return True


class InvoiceApp(BaseApp):
    """Invoice App"""
    def __init__(self, interval):
        super().__init__(interval)
        self._sheet = None
        self.connection = connection.get('app')

    @property
    def sheet(self):
        if self._sheet is None:
            self._sheet = sheet.get(settings.g('invoice_sheet'))
        return self._sheet

    def get_invoices(self):
        sql = "SELECT n, id, act FROM MGS WHERE subject = 1 ORDER BY n"
        query = self.connection.execute(sql)
        invoices = list()
        while query.next():
            invoices.append(InvoiceModel(self.connection, query.value(0), query.value(1), query.value(2)))
        query.clear()
        return invoices

    def _do(self):
        inserted = 0
        updated = 0
        deleted = 0
        report = list()
        for invoice in self.get_invoices():
            # find invoice on sheet
            cell = self.sheet.find(str(invoice.invoice_id), in_column=1)
            if invoice.action == 2:
                # check for cell:
                # if invoice exists on sheet just update
                # otherwise append new row
                if cell:
                    self.sheet.update('A{}:K{}'.format(cell.row, cell.row), [invoice.serialize()])
                    updated += 1
                else:
                    self.sheet.append_row(invoice.serialize())
                    inserted += 1
            else:
                # check for cell if invoice exists, just delete it
                # otherwise do nothing...
                if cell:
                    self.sheet.delete_row(cell.row)
                    deleted += 1
            # remove current invoice from MGS table
            invoice.done()
        # generate report
        if inserted:
            report.append('{} new invoice inserted'.format(inserted))
        if updated:
            report.append('{} invoice updated'.format(updated))
        if deleted:
            report.append('{} invoice deleted'.format(deleted))
        if report:
            return {
                'title': 'Invoice',
                'message': '\n'.join(report)
            }
