from .base import BaseModel


class MGS(BaseModel):
    """MGS Model"""

    __NAME__ = 'MGS'
    __TABLE__ = 'MGS'
    __PK_FIELD__ = 'n'

    N =         0
    ID =        1
    SUBJECT =   2
    ACT =       3

    FIELDS = [
        N,
        ID,
        SUBJECT,
        ACT
    ]

    # subject
    INVOICE =   1
    CUSTOMER =  2
    CALL =      3

    # action
    INSERT =    1
    UPDATE =    2
    DELETE =    3

    def __init__(self, n, id, subject, act):
        self.n = n
        self.id = id
        self.subject = subject
        self.act = act
    
    @property
    def pk(self):
        return self.n

    @classmethod
    def get_customers(cls):
        sql = "SELECT * FROM {} WHERE Subject=? ORDER BY {}".format(cls.__TABLE__, cls.__PK_FIELD__)
        query = cls.connection.execute(sql,  [cls.CUSTOMER])
        return cls._fetch_all(query)

    @classmethod
    def get_calls(cls):
        sql = "SELECT * FROM {} WHERE Subject=? ORDER BY {}".format(cls.__TABLE__, cls.__PK_FIELD__)
        query = cls.connection.execute(sql, [cls.CALL])
        return cls._fetch_all(query)

    @classmethod
    def get_invoices(cls):
        sql = "SELECT * FROM {} WHERE Subject=? ORDER BY {}".format(cls.__TABLE__, cls.__PK_FIELD__)
        query = cls.connection.execute(sql, [cls.INVOICE])
        return cls._fetch_all(query)
