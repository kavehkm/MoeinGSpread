# internal
from .base import BaseModel


class Invoice(BaseModel):
    """Invoice Model"""

    __NAME__ = 'Invoice'
    __TABLE__ = 'Factor1'
    __PK_FIELD__ = 'ID'

    ID =        0
    FISH_NO =   1
    DATE =      2
    TIME =      3
    SEND_TIME = 4
    INFO =      5
    TOTAL =     6
    CODE =      7
    NAME =      8
    TEL =       9
    ADDRESS =   10

    FIELDS = [
        ID,
        FISH_NO,
        DATE,
        TIME,
        SEND_TIME,
        INFO,
        TOTAL,
        CODE,
        NAME,
        TEL,
        ADDRESS,
    ]

    def __init__(
        self, id, fish_no, date, time, send_time,
        info, total, code, name, tel, address
    ):
        self.id = id
        self.fish_no = fish_no
        self.date = date
        self.time = time
        self.send_time = send_time
        self.info = info
        self.total = total
        self.code = code
        self.name = name
        self.tel = tel
        self.address = address
    
    @staticmethod
    def _sql_select():
        return """
            f.ID, f.FishNo, f.Date, f.Time, f.SendTime,
            f.Info, f.JamKol, a.Code, ISNULL(f.MiddleMan, a.Name),
            ISNULL(f.Tel, a.Tel), ISNULL(f.Address, a.Address)
        """

    @classmethod
    def _sql_from(cls):
        return """
            Factor1 AS f
            INNER JOIN AshkhasList AS a
            ON f.IDShakhs = a.ID
        """

    @classmethod
    def _sql_where(cls):
        return 'f.ID = ?'

    @property
    def pk(self):
        return self.id
    
    @property
    def items(self):
        sql = """
            SELECT k.Name, f.Tedad
            FROM Faktor2 AS f
            INNER JOIN KalaList AS k ON k.ID = f.IDKala
            WHERE f.FactorID = ?
        """
        invoice_items = []
        query = self.connection.execute(sql, [self.pk])
        while query.next():
            item = {
                'name': query.value(0),
                'quantity': int(query.value(1))
            }
            invoice_items.append(item)
        query.clear()
        return invoice_items
