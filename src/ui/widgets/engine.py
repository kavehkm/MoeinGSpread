# standard
from threading import Event
# internal
from src import settings
from .base import BaseWidget
from src.apps import InvoiceApp, CustomerApp
# pyqt
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal


##########
# Engine #
##########
class EngineSignals(QObject):
    """Engine Signals"""
    error = pyqtSignal(object)
    notification = pyqtSignal(str, str)


class Engine(QThread):
    """Engine"""
    def __init__(self, apps, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # event
        self.stopEvent = Event()
        self.resumeEvent = Event()
        # signals
        self.signals = EngineSignals()
        # apps
        self._apps = apps

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
        for app in self._apps:
            report = app.run()
            if report:
                self.signals.notification.emit(report['title'], report['message'])

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
        self.engine = Engine([
            InvoiceApp(settings.g('invoice_interval')),
            CustomerApp(settings.g('customer_interval'))
        ])

    def _createWidget(self):
        # display
        self.dispaly = QLabel()
        self.dispaly.setObjectName('Display')
        self.dispaly.setAlignment(Qt.AlignCenter)
        self.generalLayout.addWidget(self.dispaly)
        # control
        self.controlLayout = QHBoxLayout()
        self.generalLayout.addLayout(self.controlLayout)
        # - start
        self.btnStart = QPushButton('Start')
        self.controlLayout.addWidget(self.btnStart)
        # - stop
        self.btnStop = QPushButton('Stop')
        self.controlLayout.addWidget(self.btnStop)
        # default state
        self.engineFinishedHandler()

    def _connectSignals(self):
        self.btnStart.clicked.connect(self.start)
        self.btnStop.clicked.connect(self.stop)
        # engine
        self.engine.started.connect(self.engineStartedHandler)
        self.engine.finished.connect(self.engineFinishedHandler)
        self.engine.signals.error.connect(self.engineErrorHandler)
        self.engine.signals.notification.connect(self.engineNotificationHandler)

    def _setStyles(self):
        self.setStyleSheet("""
            #Display{
                font-size: 20px;
                font-weight: bold;
            }
        """)

    def start(self):
        self.engine.start()

    def stop(self):
        self.engine.stop()

    def engineStartedHandler(self):
        self.btnStart.setDisabled(True)
        self.btnStop.setEnabled(True)
        self.dispaly.setText('Running...')

    def engineFinishedHandler(self):
        self.btnStart.setEnabled(True)
        self.btnStop.setDisabled(True)
        self.dispaly.setText('Stopped.')

    def engineConnectingHandler(self):
        self.btnStart.setDisabled(True)
        self.btnStop.setDisabled(True)
        self.dispaly.setText('Connecting...')

    def engineErrorHandler(self, error):
        # stop engine
        self.engine.stop()
        # show notification
        self.ui.showNotification('ERROR', str(error))

    def engineNotificationHandler(self, title, message):
        self.ui.showNotification(title, message)

    def networkCheckerTikHandler(self, tik):
        pass

    def networkCheckerConnectedHandler(self):
        pass
