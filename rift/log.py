import logging

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('Rift')


def get_logger():
    return LOG
