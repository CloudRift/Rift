# ensure we monkeypatch before we try to connect to mongodb in
# rift.data.handler. otherwise, the tests will hang trying to connect to mongo.
import mongomock
import pymongo
pymongo.MongoClient = mongomock.MongoClient
