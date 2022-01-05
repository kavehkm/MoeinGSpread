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


#############
# Functions #
#############
def get_invoice(connection, invoice_id):
    sql = """
        SELECT ID, FishNo, Date, Time, tel, Address, MiddleMan, SendTime, Info, JamKol, IDShakhs
        FROM Factor1
        WHERE FishNo is NOT NULL AND ID = {}
    """
    query = QSqlQuery(connection)
    if not query.exec(sql.format(invoice_id)):
        raise Exception('Cannot get invoice {}'.format(invoice_id))
    if not query.next():
        return None
    return Invoice(
        query.value(0),
        query.value(1),
        query.value(2),
        query.value(3),
        query.value(4),
        query.value(5),
        query.value(6),
        query.value(7),
        query.value(8),
        query.value(9),
        query.value(10)
    )


def all_invoices(connection, last_id=0):
    sql = """
        SELECT ID, FishNo, Date, Time, Tel, Address, MiddleMan, SendTime, Info, JamKol, IDShakhs
        FROM Factor1
        WHERE FishNo is NOT NULL AND ID > {}
    """
    query = QSqlQuery(connection)
    if not query.exec(sql.format(last_id)):
        raise Exception('Cannot get invoices from database')
    invoices = list()
    while query.next():
        invoices.append(
            Invoice(
                query.value(0),
                query.value(1),
                query.value(2),
                query.value(3),
                query.value(4),
                query.value(5),
                query.value(6),
                query.value(7),
                query.value(8),
                query.value(9),
                query.value(10)
            )
        )
    query.clear()
    return invoices


def invoice_items(connection, invoice):
    sql = """
        SELECT k.Name, f.Tedad
        FROM Faktor2 AS f
        INNER JOIN KalaList AS k ON k.ID = f.IDKala
        WHERE FactorID = {}
    """
    query = QSqlQuery(connection)
    if not query.exec(sql.format(invoice.id)):
        raise Exception('Cannot get items for invoice {}'.format(invoice.id))
    items = list()
    while query.next():
        items.append('{} * {}'.format(query.value(0), int(query.value(1))))
    query.clear()
    return '\n'.join(items)


def customer_info(connection, invoice):
    if invoice.customer_id == 1:
        return
    sql = """
        SELECT Name, Tel, Address
        FROM AshkhasList
        WHERE ID = {}
    """
    query = QSqlQuery(connection)
    if not query.exec(sql.format(invoice.customer_id)):
        raise Exception('Cannot get customer information for invoice {}'.format(invoice.id))
    while query.next():
        invoice.name = invoice.name or query.value(0)
        invoice.tel = invoice.tel or query.value(1)
        invoice.address = invoice.address or query.value(2)
    query.clear()
    return True


def register_invoice(connection, invoice, loc):
    sql = "INSERT INTO GSpread(id, fishno, loc) VALUES({}, {}, '{}')"
    query = QSqlQuery(connection)
    if not query.exec(sql.format(invoice.id, invoice.fishno, loc)):
        raise Exception('Cannot register invoice {}'.format(invoice.id))
    query.clear()
    return True


def unregister_invoice(connection, invoice_id):
    query = QSqlQuery(connection)
    # get all location
    sql = 'SELECT loc FROM GSpread WHERE id >= {}'
    if not query.exec(sql.format(invoice_id)):
        raise Exception('Cannot get locations')
    locations = list()
    while query.next():
        locations.append(query.value(0))
    # delete invoice
    sql = "DELETE FROM GSpread WHERE id = {}"
    if not query.exec(sql.format(invoice_id)):
        raise Exception('Cannot unregister invoice {}'.format(invoice_id))
    # adjust locations
    sql = "SELECT id FROM GSpread WHERE id > {}"
    if not query.exec(sql.format(invoice_id)):
        raise Exception('Cannot load adjust requireds for invoice {}'.format(invoice_id))
    query2 = QSqlQuery(connection)
    sql2 = "UPDATE GSpread SET loc = '{}' WHERE id = {}"
    counter = 0
    while query.next():
        if not query2.exec(sql2.format(locations[counter], query.value(0))):
            raise Exception('Cannot adjust location for invoice {}'.format(query.value(0)))
        counter += 1
    query2.clear()
    query.clear()
    return True


def update_registered_invoice(connection, invoice_id):
    sql = "UPDATE GSpread SET is_updated = 0 WHERE id = {}"
    query = QSqlQuery(connection)
    if not query.exec(sql.format(invoice_id)):
        raise Exception('Cannot update registered invoice {}'.format(invoice_id))
    query.clear()
    return True


def update_required(connection):
    sql = "SELECT id, loc FROM GSpread WHERE is_updated = 1"
    query = QSqlQuery(connection)
    if not query.exec(sql):
        raise Exception('Cannot get update required invoices')
    ur = list()
    while query.next():
        ur.append({
            'id': query.value(0),
            'loc': query.value(1)
        })
    query.clear()
    return ur


def delete_required(connection):
    sql = "SELECT id, loc FROM Gspread WHERE is_deleted = 1"
    query = QSqlQuery(connection)
    if not query.exec(sql):
        raise Exception('Cannot get delete required invoices')
    dr = list()
    while query.next():
        dr.append({
            'id': query.value(0),
            'loc': query.value(1)
        })
    query.clear()
    return dr


##########
# Models #
##########
class Invoice(object):
    """Invoice Model"""
    def __init__(self, id, fishno, date, time, tel, address, name, send_time, info, total, customer_id):
        self.id = id
        self.fishno = fishno
        self.date = date
        self.time = time
        self.tel = tel
        self.address = address
        self.name = name
        self.send_time = send_time
        self.info = info
        self.total = total
        self.customer_id = customer_id
    
    def as_list(self):
        return [
            self.id,
            self.fishno,
            self.date,
            self.time,
            self.tel,
            self.address,
            self.name,
            self.send_time,
            self.info,
            self.total
        ]


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
        # last invoice id
        self.last_invoice_id = 0

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
            server = '.\Moein1'
            database = 'Moein'
            username = 'sa'
            password = 'arta1'
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
        # delete
        for dr in delete_required(self.connection):
            index = int(dr['loc'][1])
            self.sheet.delete_row(index)
            unregister_invoice(self.connection, dr['id'])
        # update
        for ur in update_required(self.connection):
            invoice = get_invoice(self.connection, ur['id'])
            customer_info(self.connection, invoice)
            row = invoice.as_list()
            row.append(invoice_items(self.connection, invoice))
            self.sheet.update(ur['loc'], [row])
            update_registered_invoice(self.connection, ur['id'])
        # insert
        for invoice in all_invoices(self.connection, self.last_invoice_id):
            customer_info(self.connection, invoice)
            row = invoice.as_list()
            row.append(invoice_items(self.connection, invoice))
            g_row = self.sheet.append_row(row)
            location = g_row['updates']['updatedRange'].split('!')[1]
            register_invoice(self.connection, invoice, location)
            self.last_invoice_id = invoice.id

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


#################
# Engine Widget #
#################
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
