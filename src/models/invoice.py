# internal
from .base import BaseModel


class Invoice(BaseModel):
    """Invoice Model"""

    NAME = 'Invoice'
    TABLE = 'Factor1'
    PK_FIELD = 'ID'