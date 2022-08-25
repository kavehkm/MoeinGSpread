# internal
from src import settings

# pyqt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


# connections registry
_CONNECTIONS = dict()


# connection wrapper
class Connection(object):
    """Database Connection"""
    def __init__(self, conn):
        self._conn = conn

    def execute(self, sql, parameters=()):
        query = QSqlQuery(self._conn)
        query.prepare(sql)
        for param in parameters:
            query.addBindValue(param)
        if query.exec():
            return query
        query_error = query.lastError()
        raise Exception('Database Error: {}'.format(query_error.databaseText()))


# create connection
def create(connection_name):
    server = settings.g('database_server')
    username = settings.g('database_username')
    password = settings.g('database_password')
    database = settings.g('database_name')
    connection = QSqlDatabase.addDatabase('QODBC', connection_name)
    connection.setDatabaseName(
        'driver={SQL Server};server=%s;database=%s;uid=%s;pwd=%s' % (
            server, database, username, password
        )
    )
    return connection.open(), connection


# get connection
def get(name):
    if name in _CONNECTIONS:
        return _CONNECTIONS[name]
    _, conn = create(name)
    connection = Connection(conn)
    _CONNECTIONS[name] = connection
    return connection
