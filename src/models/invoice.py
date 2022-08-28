# internal
from .base import BaseModel


class Invoice(BaseModel):
    """Invoice Model"""

    __NAME__ = 'Invoice'
    __TABLE__ = 'Factor1'
    __PK_FIELD__ = 'ID'