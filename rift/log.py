import logging


logger = logging.getLogger()


def set_logger():
    logger.addHandler(logging.StreamHandler)
    # TODO(jmv) Fix logging
    # logger.level = conf
