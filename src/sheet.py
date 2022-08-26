# internal
from src import confs

# external
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# sheets registry
_SHEETS = dict()


# sheet wrapper
class Sheet(object):
    """Sheet"""

    def __init__(self, name, pk_column=1):
        self._name = name
        self.pk_column = pk_column
        self._sheet = None

    @property
    def sheet(self):
        if self._sheet is None:
            credential_file = confs.GOOGLE_CREDENTIALS_FILE
            credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file)
            client = gspread.authorize(credentials)
            self._sheet = client.open(self._name).sheet1
        return self._sheet
    
    def find(self, pk):
        cell = self.sheet.find(str(pk), in_column=self.pk_column)
        if not cell:
            return None
        return cell.row

    def append(self, record):
        self.sheet.append_row(record)

    def update(self, pk, record):
        row = self.find(pk)
        if row is None:
            self.append(record)
        else:
            self.sheet.delete_row(row)
            self.sheet.insert_row(record, row)

    def delete(self, pk):
        row = self.find(pk)
        if row is None:
            return
        self.sheet.delete_row(row)

    def __str__(self):
        return self._name


def get(name):
    # check registry for name
    if name in _SHEETS:
        return _SHEETS[name]
    # sheet does not exists:
    # 1) create
    # 2) register
    # 3) return
    sheet = Sheet(name)
    _SHEETS[name] = sheet
    return sheet
