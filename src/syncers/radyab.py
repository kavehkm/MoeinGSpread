# internal
from src import settings
from .base import BaseSyncer

# external
import requests


class API(object):
    """Iran Radyab API"""

    def __init__(self, version, key):
        self._version = version
        self._key = key
    
    def _request(self, command):
        params = {
            'api': 'user',
            'ver': self._version,
            'key': self._key,
            'cmd': command
        }

        base_url = 'http://pro.iranradyab.com/api/api.php'

        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            raise Exception('Cannot complete request cause of: {}'.format(response.text))

        return response.json()

    def all_couriers(self):
        return self._request('USER_GET_OBJECTS')

    def get_courier_last_location(self, courier_ids):
        return self._request('OBJECT_GET_LOCATIONS,d{}'.format(';'.join(courier_ids)))


class Radyab(BaseSyncer):
    """Iran Radyab"""

    TARGETS = settings.g('radyab_targets', [])

    def __init__(self, interval):
        super().__init__(interval)
        self.api = API(
            settings.g('radyab_version'),
            settings.g('radyab_key')
        )

    def targets_set(self, range_str, records):
        for target in self.targets:
            target.set(range_str, records)
    
    def _upload(self):
        couriers = self.api.all_couriers()
        ids = [courier['imei'] for courier in couriers]
        locations = self.api.get_courier_last_location(ids)

        records = []

        for courier in couriers:
            imei = courier['imei']
            name = courier['name']
            location = locations.get(imei, {})
            records.append([
                imei,
                name,
                location.get('lat', 0),
                location.get('lng', 0),
                location.get('altitude', 0),
                location.get('angle', 0),
                location.get('speed', 0)
            ])
        
        self.targets_set('A2:I20', records)
