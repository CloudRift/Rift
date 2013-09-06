import logging


logger = logging.getLogger()


def set_logger():
    logger.addHandler(logging.StreamHandler)
    logger.level = conf