# internal
from src import connection


class BaseModel(object):
    """Base Model"""

    __NAME__ = 'Base'
    __TABLE__ = 'Base_TABLE'
    __PK_FIELD__ = 'ID'

    FIELDS = ()

    # default connection reference
    connection = connection.get()

    @staticmethod
    def _sql_select():
        return '*'

    @classmethod
    def _sql_from(cls):
        return cls.__TABLE__
    
    @classmethod
    def _sql_where(cls):
        return '{}=?'.format(cls.__PK_FIELD__)

    @classmethod
    def _fetch(cls, query):
        if not query.next():
            return None
        record = [query.value(field) for field in cls.FIELDS]
        query.clear()
        return cls(*record)

    @classmethod
    def _fetch_all(cls, query):
        objects = []
        while query.next():
            record = [query.value(field) for field in cls.FIELDS]
            objects.append(cls(*record))
        query.clear()
        return objects

    @classmethod
    def all(cls):
        sql = 'SELECT {} FROM {};'.format(
            cls._sql_select(),
            cls._sql_from()
        )
        query = cls.connection.execute(sql)
        return cls._fetch_all(query)

    @classmethod
    def get(cls, pk):
        sql = 'SELECT {} FROM {} WHERE {};'.format(
            cls._sql_select(),
            cls._sql_from(),
            cls._sql_where()
        )
        params = [pk]
        query = cls.connection.execute(sql, params)
        obj = cls._fetch(query)
        if obj is None:
            raise Exception('{} with {} does not exists'.format(cls.__NAME__, pk))
        return obj

    @property
    def pk(self):
        return getattr(self, self.__PK_FIELD__)

    def delete(self):
        sql = 'DELETE {} WHERE {}=?'.format(
            self.__TABLE__,
            self.__PK_FIELD__,
        )
        params = [self.pk]
        query = self.connection.execute(sql, params)
        query.clear()
