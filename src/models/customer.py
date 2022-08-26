# internal
from .base import BaseModel


class Customer(BaseModel):
    """Customer Model"""

    NAME = 'Customer'
    TABLE = 'AshkhasList'
    PK_FIELD = 'ID'
