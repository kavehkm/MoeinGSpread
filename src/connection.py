# internal
from src import confs, settings

# pyqt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


# connections registry
_CONNECTIONS = dict()


# connection wrapper
class Connection(object):
    """Database Connection"""
    def __init__(self, name):
        self._name = name
        self._conn = None

    @property
    def conn(self):
        if self._conn is None:
            server = settings.g('database_server')
            username = settings.g('database_username')
            password = settings.g('database_password')
            database = settings.g('database_name')
            connection = QSqlDatabase.addDatabase('QODBC', self._name)
            connection.setDatabaseName(
                'driver={SQL Server};server=%s;database=%s;uid=%s;pwd=%s' % (
                    server, database, username, password
                )
            )
            connection.open()
            self._conn = connection
        return self._conn

    def execute(self, sql, parameters=()):
        query = QSqlQuery(self.conn)
        query.prepare(sql)
        for param in parameters:
            query.addBindValue(param)
        if query.exec():
            return query
        query_error = query.lastError()
        raise Exception('Database Error: {}'.format(query_error.databaseText()))


def get(name=confs.DEFAULT_CONNECTION_NAME):
    if name in _CONNECTIONS:
        return _CONNECTIONS[name]
    connection = Connection(name)
    _CONNECTIONS[name] = connection
    return connection
