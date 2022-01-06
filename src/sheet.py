# internal
from src import confs
# external
import gspread
from oauth2client.service_account import ServiceAccountCredentials


_SHEETS = dict()


def get(name):
    if name in _SHEETS:
        return _SHEETS[name]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(confs.GOOGLE_CREDENTIALS_FILE)
    client = gspread.authorize(credentials)
    sheet = client.open(name).sheet1
    _SHEETS[name] = sheet
    return sheet
