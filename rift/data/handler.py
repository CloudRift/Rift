from rift.data.adapters import mongodb
from rift import log

_db_handler = mongodb.MongoDB()

try:
    _db_handler.connect()
except Exception as e:
    log.get_logger().error("Problem connecting to MongoDB: %s", e)


def get_handler():
    return _db_handler
