# standard
from time import time

# internal
from src import sheet
from src.models import MGS


class BaseSyncer(object):
    """Base Syncer"""

    MODEL = None
    TARGETS = None
    TRACKER = None
    SUBJECT = None
    
    def __init__(self, interval):
        self._interval = interval
        self._ran = 0
        self._model = None
        self._targets = None
        self._tracker = None
        self._reports = []
    
    @property
    def targets(self):
        if self._targets is None:
            self._targets = [
                sheet.get(name)
                for name in self.TARGETS
            ]
        return self._targets

    @property
    def tracker(self):
        if self._tracker is None:
            self._tracker = sheet.get(self.TRACKER)
        return self._tracker
    
    @staticmethod
    def filter(record):
        for i in range(len(record)):
            value = record[i]
            if isinstance(value, str):
                value = value.strip()
            if value == '' or value is None:
                record[i] = 'NULL'
        return record

    def serialize(self, instance):
        return instance

    def flush_reports(self):
        pass

    def _download(self):
        pass

    def _upload(self): 
        for log in MGS.filter_by_subject(self.SUBJECT):
            args = ()
            kwargs = {}
            method = None
            # dispatch log
            if log.act == MGS.INSERT:
                instance = self.MODEL.get(log.id)
                method = 'append'
                args = (self.filter(self.serialize(instance)),)
            elif log.act == MGS.UPDATE:
                instance = self.MODEL.get(log.id)
                method = 'update'
                args = (instance.pk, self.filter(self.serialize(instance)))
            elif log.act == MGS.DELETE:
                method = 'delete'
                args = (log.id,)
            # update targets
            for target in self.targets:
                getattr(target, method)(*args, **kwargs)
            # delete log
            log.delete()

    def _do(self):
        self._download()
        self._upload()

    def run(self):
        if time() - self._ran > self._interval:
            self._do()
            self._ran = time()
