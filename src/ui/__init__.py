# internal
from src import confs
from src.ui.widgets import EngineWidget
# pyqt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSystemTrayIcon, QMenu


class UI(QMainWindow):
    """User Interface"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # bootstraping
        self._bootstrap()

    def _bootstrap(self):
        self._createUI()
        self._createTray()
        self._connectSignals()

    def _createUI(self):
        # central widget
        self.centWidget = QWidget(self)
        self.setCentralWidget(self.centWidget)
        # general layout
        self.generalLayout = QHBoxLayout()
        self.centWidget.setLayout(self.generalLayout)
        # title
        self.setWindowTitle('MGS')
        # icon
        self.setWindowIcon(QIcon('{}/{}'.format(confs.RESOURCE_DIR, 'gsheet.png')))
        # fix size
        self.setFixedSize(170, 75)
        # engine widget
        self.engineWidget = EngineWidget(self)
        self.generalLayout.addWidget(self.engineWidget)

    def _createTray(self):
        # tray
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('{}/{}'.format(confs.RESOURCE_DIR, 'gsheet.png')))
        self.tray.setToolTip('MGS')
        self.tray.setVisible(True)
        # menu
        menu = QMenu()
        menu.addAction('Show/Hide', self.trayShowHideAction)
        menu.addAction('Quit', self.trayQuitAction)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.trayActivatedHandler)

    def trayShowHideAction(self):
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()

    def trayActivatedHandler(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

    def trayQuitAction(self):
        self.close()

    def closeEvent(self, event):
        if self.isVisible():
            self.hide()
            event.ignore()
        else:
            self.close()

    def _connectSignals(self):
        pass

    def showNotification(self, title, message):
        self.tray.showMessage(title, message, QSystemTrayIcon.NoIcon)
