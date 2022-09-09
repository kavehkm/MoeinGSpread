# internal
from src import settings
from .base import BaseSyncer
from src.models import Customer, MGS
from src.utils import split_tels, null_to_none


class Customer(BaseSyncer):
    """Customer Syncer"""

    MODEL = Customer
    SUBJECT = MGS.CUSTOMER
    TRACKER = settings.g('customer_tracker')
    TARGETS = settings.g('customer_targets', [])

    def serialize(self, instance):
        record = [
            instance.id,
            instance.code,
            instance.prefix,
            instance.first_name,
            instance.last_name,
            instance.email,
            instance.state,
            instance.city,
            instance.address,
            instance.post_code,
            instance.company,
            instance.company_address,
            instance.info,
            instance.group_name
        ]
        for tel in split_tels(instance.tels):
            record.append(tel)
        return record

    def _download(self):
        # set main target
        target = self.targets[0]
        # download all update logs
        logs = self.tracker.get_all_records()
        for log in logs:
            # get updated record, clean and collect data
            record = list(map(null_to_none, target.get_record(log[0])))
            data = {
                'id': 0,
                'code': 1,
                'prefix': 2,
                'first_name': 3,
                'last_name': 4,
                'email': 5,
                'state': 6,
                'city': 7,
                'address': 8,
                'post_code': 9,
                'company': 10,
                'company_address': 11,
                'info': 12,
                'group_name': 13
            }
            for key, value in data.items():
                try:
                    data[key] = record[value]
                except Exception:
                    data[key] = ''
            # - get tels
            tels = []
            try:
                for tel in record[14:]:
                    if tel:
                        tels.append(tel)
            except Exception:
                pass
            data['tels'] = tels

            # find customer and update
            customer = self.MODEL.get(data['id'])
            customer.update(data)
            # delete tracker log
            self.tracker.delete_record(1)
            # delete mgs logs
            MGS.delete_customers(data['id'])
