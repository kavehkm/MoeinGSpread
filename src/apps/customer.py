# internal
from src import sheet
from src import settings
from .base import BaseApp
from src import connection


class CustomerModel(object):
    """Customer Model"""
    def __init__(self, connection, n, customer_id, action):
        self.connection = connection
        self.n = n
        self.action = action
        self.customer_id = customer_id
        self.code = None
        self.name = None
        self.tel = None
        self.email = None
        self.state = None
        self.city = None
        self.address = None
        self.post_code = None
        self.company = None
        self.company_address = None
        self.info = None
        self.group = None
        # check for full initialize
        if action != 3:
            self._init()

    def _init(self):
        sql = """
            SELECT a.Code, a.Name, a.Tel, a.Email, a.State, a.City,
            a.Address, a.Posti, a.Company, a.CompanyAddress, a.info, g.Caption
            FROM AshkhasList AS a
            LEFT OUTER JOIN GroupAshkhas AS g ON a.GroupID = g.ID
            WHERE a.ID = ?
        """
        query = self.connection.execute(sql, [self.customer_id])
        if not query.next():
            raise Exception('Customer {} does not exists'.format(self.customer_id))
        # initialization
        self.code = query.value(0)
        self.name = query.value(1)
        self.tel = query.value(2)
        self.email = query.value(3)
        self.state = query.value(4)
        self.city = query.value(5)
        self.address = query.value(6)
        self.post_code = query.value(7)
        self.company = query.value(8)
        self.company_address = query.value(9)
        self.info = query.value(10)
        self.group = query.value(11)
        query.clear()

    def serialize(self):
        tels = list()
        try:
            tels = self.tel.replace(' ', '').split('-')
        except Exception:
            pass

        return [
            self.customer_id,
            self.code,
            self.name,
            '\n'.join(tels) or self.tel,
            self.email,
            self.state,
            self.city,
            self.address,
            self.post_code,
            self.company,
            self.company_address,
            self.info,
            self.group
        ]

    def done(self):
        sql = "DELETE FROM MGS WHERE n = ? AND id = ?"
        query = self.connection.execute(sql, [self.n, self.customer_id])
        query.clear()
        return True


class CustomerApp(BaseApp):
    """Customer App"""
    def __init__(self, interval):
        super().__init__(interval)
        self._sheet = None
        self.connection = connection.get('app')

    @property
    def sheet(self):
        if self._sheet is None:
            self._sheet = sheet.get(settings.g('customer_sheet'))
        return self._sheet

    def get_customers(self):
        sql = "SELECT n, id, act FROM MGS WHERE subject = 2 ORDER BY n"
        query = self.connection.execute(sql)
        customers = list()
        while query.next():
            customers.append(CustomerModel(self.connection, query.value(0), query.value(1), query.value(2)))
        query.clear()
        return customers

    def _do(self):
        inserted = 0
        updated = 0
        deleted = 0
        report = list()
        for customer in self.get_customers():
            cell = self.sheet.find(str(customer.customer_id), in_column=1)
            if customer.action == 1:
                self.sheet.append_row(customer.serialize())
                inserted += 1
            elif customer.action == 2:
                if cell:
                    self.sheet.update('A{}:M{}'.format(cell.row, cell.row), [customer.serialize()])
                    updated += 1
                else:
                    self.sheet.append_row(customer.serialize())
                    inserted += 1
            else:
                if cell:
                    self.sheet.delete_row(cell.row)
                    deleted += 1
            customer.done()
        if inserted:
            report.append('{} new customer inserted'.format(inserted))
        if updated:
            report.append('{} customer updated'.format(updated))
        if deleted:
            report.append('{} customer deleted'.format(deleted))
        if report:
            return {
                'title': 'Customer',
                'message': '\n'.join(report)
            }
