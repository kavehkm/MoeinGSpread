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
                'id': record[0],
                'code': record[1],
                'prefix': record[2],
                'first_name': record[3],
                'last_name': record[4],
                'email': record[5],
                'state': record[6],
                'city': record[7],
                'address': record[8],
                'post_code': record[9],
                'company': record[10],
                'company_address': record[11],
                'info': record[12],
                'group_name': record[13],
                'tels': [tel for tel in record[14:] if tel]
            }
            # find customer and update
            customer = self.MODEL.get(data['id'])
            customer.update(data)
            # delete tracker log
            self.tracker.delete_record(1)
            # delete mgs logs
            MGS.delete_customers(data['id'])
