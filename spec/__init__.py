# ensure we monkeypatch before we try to connect to mongodb in
# rift.data.handler. otherwise, the tests will hang trying to connect to mongo.
import mongomock
import pymongo
pymongo.MongoClient = mongomock.MongoClient

# mock out the load_secret_key function, which normally looks for a file
from cryptography.fernet import Fernet
import rift.data.common
rift.data.common.load_secret_key = lambda: Fernet.generate_key()
