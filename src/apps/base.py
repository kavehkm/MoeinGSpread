# standard
from time import time


class BaseApp(object):
    """Base Application"""
    def __init__(self, interval):
        self._ran = 0
        self._interval = interval

    def _do(self):
        # main functionality of app
        pass

    def run(self):
        # check for period
        if time() - self._ran > self._interval:
            self._do()
            # save ran time
            self._ran = time()
