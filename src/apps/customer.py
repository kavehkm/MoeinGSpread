# internal
from .base import BaseApp, BaseModel
from src.utils import split_tels


class CustomerModel(BaseModel):
    """Customer Model"""
    def __init__(self, *args, **kwargs):
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
        super().__init__(*args, **kwargs)

    def _init(self):
        sql = """
            SELECT a.Code, a.Name, a.Tel, a.Email, a.State, a.City,
            a.Address, a.Posti, a.Company, a.CompanyAddress, a.info, g.Caption
            FROM AshkhasList AS a
            LEFT OUTER JOIN GroupAshkhas AS g ON a.GroupID = g.ID
            WHERE a.ID = ?
        """
        query = self.connection.execute(sql, [self.model_id])
        if not query.next():
            raise Exception('Customer {} does not exists'.format(self.model_id))
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
        record = [
            self.model_id,
            self.code,
            self.name,
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
        tels = split_tels(self.tel)
        if tels:
            record.extend(tels)
        return record


class CustomerApp(BaseApp):
    """Customer App"""
    SUBJECT = 2
    NAME = 'Customer'
    MODEL = CustomerModel
