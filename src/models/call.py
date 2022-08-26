# internal
from .base import BaseModel


class Call(BaseModel):
    """Call Model"""

    NAME = 'Call'
    TABLE = 'viwCallHistory'
    PK_FIELD = 'ID'

    ID =                0
    DATE =              1
    TIME =              2
    LINE =              3
    NUMBER =            4
    USER_ID =           5
    USER_NAME =         12
    ACCEPT =            6
    CUSTOMER_ID =       7
    CUSTOMER_CODE =     8
    CUSTOMER_NAME =     10
    CUSTOMER_ADDRESS =  11

    FIELDS = (
        ID,
        DATE,
        TIME,
        LINE,
        NUMBER,
        USER_ID,
        USER_NAME,
        ACCEPT,
        CUSTOMER_ID,
        CUSTOMER_CODE,
        CUSTOMER_NAME,
        CUSTOMER_ADDRESS
    )    

    def __init__(
        self, id, date, time, line, number, user_id, user_name,
        accept, customer_id, customer_name, customer_address
    ):
        self.id = id
        self.date = date
        self.time = time
        self.line = line
        self.number = number
        self.user_id = user_id
        self.user_name = user_name
        self.accept = accept
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_address = customer_address
