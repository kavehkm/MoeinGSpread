# standard
import os
# internal
from src.confs import RESOURCE_DIR


def get(name):
    return os.path.join(RESOURCE_DIR, name)
