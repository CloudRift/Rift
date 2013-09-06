from rift.data.adapters import mongodb

_db_handler = mongodb.MongoDB()
_db_handler.connect()


def get_handler():
    return _db_handler
