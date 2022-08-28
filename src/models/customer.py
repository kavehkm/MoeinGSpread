# internal
from .base import BaseModel


class Customer(BaseModel):
    """Customer Model"""

    __NAME__ = 'Customer'
    __TABLE__ = 'AshkhasList'
    __PK_FIELD__ = 'ID'

    ID =                0
    CODE =              1
    PREFIX =            2
    NAME =              3
    EMAIL =             4
    STATE =             5
    CITY =              6
    ADDRESS =           7
    POST_CODE =         8
    COMPANY =           9
    COMPANY_ADDRESS =   10
    TELS =              11
    INFO =              12
    GROUP_NAME =        13

    FIELDS = (
        ID,
        CODE,
        PREFIX,
        NAME,
        EMAIL,
        STATE,
        CITY,
        ADDRESS,
        POST_CODE,
        COMPANY,
        COMPANY_ADDRESS,
        TELS,
        INFO,
        GROUP_NAME
    )

    def __init__(
        self, id, code, name, prefix, email, state, city, address,
        post_code, company, company_address, tels, info, group_name
    ):
        self.id = id
        self.code = code
        self.prefix = prefix
        self.name = name
        self.email = email
        self.state = state
        self.city = city
        self.address = address
        self.post_code = post_code
        self.company = company
        self.company_address = company_address
        self.tels = tels
        self.info = info
        self.group_name = group_name

    @staticmethod
    def _sql_select():
        return """
            a.ID, a.Code, a.Name, a.Prefix, a.Email, a.State, a.City,
            a.Address, a.Posti, a.Company, a.CompanyAddress, a.Tel, a.Info, g.Caption
        """

    @classmethod
    def _sql_from(cls):
        return """
            AshkhasList AS a
            LEFT OUTER JOIN GroupAshkhas AS g
            ON a.GroupID = g.ID
        """
    
    @classmethod
    def _sql_where(cls):
        return 'a.ID=?'

    @property
    def pk(self):
        return self.id
