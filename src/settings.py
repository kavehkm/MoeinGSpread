# standard
import json

# internal
from src import confs


class API(object):
    """Settings API"""

    def __init__(self):
        self._settings = dict()
        self._initialize()

    def _initialize(self):
        try:
            with open(confs.SETTINGS_FILE, 'rt') as f:
                self._settings = json.loads(f.read())
        except Exception:
            self._settings = confs.DEFAULT_SETTINGS

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def set(self, key, value):
        self._settings[key] = value

    def save(self):
        with open(confs.SETTINGS_FILE, 'wt') as f:
            f.write(json.dumps(self._settings, indent=4))


# instance
_api = API()


# create interface
g = _api.get
s = _api.set
save = _api.save
