# standard
from threading import Event
# internal
from src import confs
from .base import BaseWidget
# pyqt
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QObject, QThread, QThreadPool, pyqtSignal
# gspread
import gspread
from oauth2client.service_account import ServiceAccountCredentials


##########
# Engine #
##########
class EngineSignals(QObject):
    """Engine Signals"""
    error = pyqtSignal(object)
    notification = pyqtSignal(str, str)


class Engine(QThread):
    """Engine"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # event
        self.stopEvent = Event()
        self.resumeEvent = Event()
        # signals
        self.signals = EngineSignals()
        # sheet and connection
        self._sheet = None
        self._connection = None

    @property
    def sheet(self):
        if self._sheet is None:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(confs.GOOGLE_CREDENTIALS_FILE)
            client = gspread.authorize(credentials)
            self._sheet = client.open('test').sheet1
        return self._sheet

    @property
    def connection(self):
        if self._connection is None:
            # database credentials
            server = '.\Moein'
            database = 'Moein'
            username = 'sa'
            password = 'arta0@'
            # create connection
            connection = QSqlDatabase.addDatabase('QODBC')
            connection.setDatabaseName(
                'driver={SQL Server};server=%s;database=%s;uid=%s;pwd=%s' % (
                    server, database, username, password
                )
            )
            # check for connection
            if not connection.open():
                raise Exception('Database connection error')
            self._connection = connection
        return self._connection

    def invoices(self):
        # create query
        query = QSqlQuery(self.connection)
        # get invoice
        sql = "SELECT * FROM ProductMap"
        if not query.exec(sql):
            raise Exception('Cannot get invoices from database')
        invoices = list()
        while query.next():
            invoices.append([query.value(0), query.value(1)])
        # clear query
        query.clear()

        return invoices

    def start(self, *args, **kwargs):
        self.resumeEvent.set()
        self.stopEvent.clear()
        super().start(*args, **kwargs)

    def stop(self):
        self.stopEvent.set()
        self.quit()
        self.resumeEvent.set()

    def resume(self):
        self.resumeEvent.set()

    def pause(self):
        self.resumeEvent.clear()

    def _do(self):
        for invoice in self.invoices():
            self.sheet.append_row(invoice)
            print(invoice, 'inserted successfully')

    def run(self):
        # do-while(stopEvent is not set)
        while True:
            try:
                self._do()
            except Exception as e:
                self.pause()
                self.signals.error.emit(e)
            # wait for resume
            self.resumeEvent.wait()
            # check for stop event
            if self.stopEvent.wait(10):
                break


class EngineWidget(BaseWidget):
    """Engine Widget"""
    def _initialize(self):
        self.engine = Engine()
        self.threadPool = QThreadPool()

    def _createWidget(self):
        # control
        # - start
        self.btnStart = QPushButton('Start')
        self.generalLayout.addWidget(self.btnStart)
        # - stop
        self.btnStop = QPushButton('Stop')
        self.btnStop.setDisabled(True)
        self.generalLayout.addWidget(self.btnStop)

    def _connectSignals(self):
        self.btnStart.clicked.connect(self.start)
        self.btnStop.clicked.connect(self.stop)
        # engine
        self.engine.started.connect(self.engineStartedHandler)
        self.engine.finished.connect(self.engineFinishedHandler)
        self.engine.signals.error.connect(self.engineErrorHandler)
        self.engine.signals.notification.connect(self.engineNotificationHandler)

    def start(self):
        self.engine.start()

    def stop(self):
        self.engine.stop()

    def engineStartedHandler(self):
        self.btnStart.setDisabled(True)
        self.btnStop.setEnabled(True)

    def engineFinishedHandler(self):
        self.btnStart.setEnabled(True)
        self.btnStop.setDisabled(True)

    def engineConnectingHandler(self):
        self.btnStart.setDisabled(True)
        self.btnStop.setDisabled(True)

    def engineErrorHandler(self, error):
        print(str(error))

    def engineNotificationHandler(self, title, message):
        print('Notification: {}: {}'.format(title, message))

    def networkCheckerTikHandler(self, tik):
        pass

    def networkCheckerConnectedHandler(self):
        pass
