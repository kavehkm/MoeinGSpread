# pyqt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class BaseWidget(QWidget):
    """Base Widget"""
    def __init__(self, ui, *args, **kwargs):
        self.ui = ui
        super().__init__(ui, *args, **kwargs)
        self._bootstrap()

    def _bootstrap(self):
        self._initialize()
        self._setLayout()
        self._createWidget()
        self._setStyles()
        self._connectSignals()

    def _initialize(self):
        pass

    def _setLayout(self):
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setAlignment(Qt.AlignTop)
        self.generalLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.generalLayout)

    def _createWidget(self):
        pass

    def _setStyles(self):
        pass

    def _connectSignals(self):
        pass
