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
