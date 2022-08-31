# standard
import time

# internal
from src import sheet


class BaseSyncer(object):
    """Base Syncer"""

    MODEL = None
    TARGETS = None
    TRACKER = None
    
    def __init__(self, interval):
        self._interval = interval
        self._ran = 0
        self._model = None
        self._targets = None
        self._tracker = None
        self._reports = []
    
    @property
    def model(self):
        if self._model is None:
            pass
        return self._model
    
    @property
    def targets(self):
        if self._targets is None:
            pass
        return self._targets

    @property
    def tracker(self):
        if self._tracker is None:
            pass
        return self._tracker

    def flush_reports(self):
        pass

    def _download(self):
        pass

    def _upload(self):
        pass

    def _do(self):
        self._download()
        self._upload()

    def run(self):
        if time() - self._ran > self._interval:
            self._do()
            self._ran = time()
