import os
import sys

from cryptography.fernet import Fernet

from rift import config
from rift import log

LOG = log.get_logger()
cfg = config.get_config()
KEY = None


def load_secret_key(filename=cfg.general.key_file):
    dev_location = './etc/rift/secret.key'
    key_path = None
    if os.path.exists(filename):
        key_path = filename
    elif os.path.exists(dev_location):
        key_path = dev_location
    else:
        LOG.error(
            ('Could not load secret key file at: %s or %s. Please add your '
             'key to one of those locations.'),
            filename,
            dev_location
        )
        sys.exit('Killing service')

    with open(key_path, 'rb') as f:
        key = f.read()

    LOG.info('Loaded secret key file from: %s', key_path)
    return key


def generate_key(filename):
    key = Fernet.generate_key()

    with open(filename, 'wb') as f:
        f.write(key)

    LOG.info('Saved key to %s', filename)


def get_secret_key():
    global KEY
    if not KEY:
        KEY = load_secret_key()
    return KEY
