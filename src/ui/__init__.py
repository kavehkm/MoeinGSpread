# internal
from src.ui.widgets import EngineWidget
# pyqt
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout


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
        self.setWindowTitle('Updater')
        # fix size
        self.setFixedSize(170, 75)
        # engine widget
        self.engineWidget = EngineWidget(self)
        self.generalLayout.addWidget(self.engineWidget)

    def _createTray(self):
        pass

    def _connectSignals(self):
        pass

    def showNotification(self, title, message):
        pass
