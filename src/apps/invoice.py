# internal
from .base import BaseApp, BaseModel
from src.utils import split_tels


class InvoiceModel(BaseModel):
    """Invoice Model"""
    def __init__(self, *args, **kwargs):
        self.fishno = None
        self.date = None
        self.time = None
        self.tel = None
        self.address = None
        self.code = None
        self.name = None
        self.send_time = None
        self.info = None
        self.total = None
        self.items = list()
        super().__init__(*args, **kwargs)

    def _init(self):
        sql = """
            SELECT f.FishNo, f.Date, f.Time, f.Tel, f.Address, f.MiddleMan,
            f.SendTime, f.Info, f.JamKol, a.Name, a.Tel, a.Address, a.Code
            FROM Factor1 AS f
            INNER JOIN AshkhasList AS a ON f.IDShakhs = a.ID
            WHERE f.ID = ? 
        """
        query = self.connection.execute(sql, [self.model_id])
        if not query.next():
            raise Exception('Invoice {} does not exists'.format(self.model_id))
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
        self.code = query.value(12)
        query.clear()
        # find invoice items
        sql = """
            SELECT k.Name, f.Tedad
            FROM Faktor2 AS f
            INNER JOIN KalaList AS k ON k.ID = f.IDKala
            WHERE f.FactorID = ?
        """
        query = self.connection.execute(sql, [self.model_id])
        while query.next():
            self.items.append([query.value(0), int(query.value(1))])
        query.clear()

    def serialize(self):
        record = [
            self.model_id,
            self.fishno,
            self.date,
            self.time,
            self.address,
            self.code,
            self.name,
            self.send_time,
            self.info,
            self.total,
            '\n'.join(['{} * {}'.format(*item) for item in self.items])
        ]
        tels = split_tels(self.tel)
        if tels:
            record.extend(tels)
        return record


class InvoiceApp(BaseApp):
    """Invoice App"""
    SUBJECT = 1
    NAME = 'Invoice'
    MODEL = InvoiceModel
