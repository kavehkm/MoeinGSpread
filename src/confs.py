# standard
import os


# project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# settings file
SETTINGS_FILE = os.path.join(BASE_DIR, 'settings.json')


# google credentials file
GOOGLE_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')


# resource dir
RESOURCE_DIR = os.path.join(BASE_DIR, 'src/ui/resources')


# default settings
DEFAULT_SETTINGS = {
    'database_server': '',
    'database_username': '',
    'database_password': '',
    'database_name': '',
    'invoice_sheet': 'invoices',
    'invoice_interval': 10,
    'customer_sheet': 'customers',
    'customer_interval': 60
}
