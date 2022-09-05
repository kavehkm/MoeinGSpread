# standard
from time import time

# internal
from src import sheet
from src.models import MGS
from src.utils import none_to_null


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
    def tracker(self):
        if self._tracker is None:
            self._tracker = sheet.get(self.TRACKER)
        return self._tracker

    @property
    def targets(self):
        if self._targets is None:
            self._targets = [
                sheet.get(name)
                for name in self.TARGETS
            ]
        return self._targets

    def targets_append(self, record):
        for target in self.targets:
            target.append(record)

    def targets_update(self, pk, record):
        for target in self.targets:
            target.update(pk, record)

    def targets_delete(self, pk):
        for target in self.targets:
            target.delete(pk)
    
    def pass_log(self, log):
        return False if log else True

    @staticmethod
    def filter(record):
        return list(map(none_to_null, record))

    def serialize(self, instance):
        return instance

    def flush_reports(self):
        pass

    def _download(self):
        pass

    def _upload(self): 
        for log in MGS.filter_by_subject(self.SUBJECT):
            # dispatch log
            if self.pass_log(log):
                pass
            elif log.act in [MGS.INSERT, MGS.UPDATE]:
                instance = self.MODEL.get(log.id)
                record = self.filter(self.serialize(instance))
                if log.act == MGS.INSERT:
                    self.targets_append(record)
                else:
                    self.targets_update(instance.pk, record)
            elif log.act == MGS.DELETE:
                self.targets_delete(log.id)
            # delete log
            log.delete()

    def _do(self):
        self._download()
        self._upload()

    def run(self):
        if time() - self._ran > self._interval:
            self._do()
            self._ran = time()
