# internal
from src.ui.widgets import EngineWidget, SettingsWidget
# pyqt
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton


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
        # show first widget
        self._menuHandler(0)

    def _createUI(self):
        # central widget
        self.centWidget = QWidget(self)
        self.setCentralWidget(self.centWidget)
        # general layout
        self.generalLayout = QHBoxLayout()
        self.centWidget.setLayout(self.generalLayout)

        # title

        # geometry

        # min-size

        # icon

        # menu
        self.menu = QWidget(self)
        self.menu.setFixedWidth(100)
        self.menuLayout = QVBoxLayout()
        self.menu.setLayout(self.menuLayout)
        self.generalLayout.addWidget(self.menu)
        # - menu buttons
        self.btnEngine = QPushButton('Engine')
        self.btnSettings = QPushButton('Settings')
        self._menuBtns = [
            self.btnEngine,
            self.btnSettings,
        ]
        for btn in self._menuBtns:
            self.menuLayout.addWidget(btn)
        self.menuLayout.addStretch(1)
        # widgets
        self.widget = QWidget(self)
        self.widgetLayout = QVBoxLayout()
        self.widget.setLayout(self.widgetLayout)
        self.generalLayout.addWidget(self.widget)
        self._widgets = [
            widgets.EngineWidget(self),
            widgets.SettingsWidget(self),
        ]
        for widget in self._widgets:
            self.widgetLayout.addWidget(widget)

    def _createTray(self):
        pass

    def _connectSignals(self):
        pass

    def _menuHandler(self, index):
        pass

    def showNotification(self, title, message):
        pass
