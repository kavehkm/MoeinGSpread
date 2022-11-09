# internal
from src import sheet
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
        self._sheet1 = None
        self._sheet2 = None

    @property
    def sheet1(self):
        if self._sheet1 is None:
            self._sheet1 = sheet.get(self.TARGETS[0])
        return self._sheet1

    @property
    def sheet2(self):
        if self._sheet2 is None:
            self._sheet2 = sheet.get(self.TARGETS[1])
        return self._sheet2
    
    def _upload(self):
        couriers = self.api.all_couriers()
        ids = [courier['imei'] for courier in couriers]
        ids.insert(0, 'placeholder!')

        locations = self.api.get_courier_last_location(ids)

        records1 = []
        records2 = []

        for courier in couriers:
            imei = courier['imei']
            name = courier['name']
            location = locations.get(imei)

            lat = location.get('lat', 0)
            long = location.get('lng', 0)
            altitude = location.get('altitude', 0)
            angle = location.get('angle', 0)
            speed = location.get('speed', 0)
            date, time = location.get('dt_server', '- -').split(' ')
            # check for location
            if location is not None:
                records1.append([imei, name, lat, long, altitude, angle, speed, date, time])
                records2.extend([name, lat, long, date, time])

        self.sheet1.set('A2:I20', records1)
        self.sheet2.insert(records2, 2)
