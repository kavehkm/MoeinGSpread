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
            instance.name,
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
                'name': record[2],
                'email': record[3],
                'state': record[4],
                'city': record[5],
                'address': record[6],
                'post_code': record[7],
                'company': record[8],
                'company_address': record[9],
                'info': record[10],
                'group_name': record[11],
                'tels': [tel for tel in record[12:] if tel]
            }
            # find customer and update
            customer = self.MODEL.get(data['id'])
            customer.update(data)
            # delete tracker log
            self.tracker.delete_record(1)
            # delete mgs logs
            MGS.delete_customers(data['id'])
