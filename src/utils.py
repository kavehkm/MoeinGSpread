# standard
import subprocess

# internal
from src import confs


def is_single_instance(app_name=confs.APP_NAME):
    cmd = 'TASKLIST /FI "IMAGENAME eq {}.exe"'.format(app_name)
    res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    tasks = res.stdout.lower()
    if tasks.count(app_name.lower()) > 1:
        return False
    return True


def split_tels(tel_string, spliter='-'):
    try:
        return tel_string.replace(' ', '').split(spliter)
    except Exception:
        return list()


def null_to_none(string):
    return None if string.lower() == 'null' else string


def none_to_null(value):
    return 'NULL' if value is None else value
