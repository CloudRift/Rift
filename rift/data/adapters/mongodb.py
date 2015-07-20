from pymongo import MongoClient

from rift.config import get_config

STATUS_NEW = 'NEW'
STATUS_CONNECTED = 'CONNECTED'
STATUS_CLOSED = 'CLOSED'

conf = get_config()


class MongoDB(object):
    """
    An handler class to provide CRUD operations using MongoDB
    """

    def __init__(self):
        """
        Sets the address of the mongo server, specifies the database to use
        and connects to the server
        """
        self.server = conf.mongodb.server
        self.database_name = conf.mongodb.database
        self.status = STATUS_NEW

    def connect(self):
        """
        Creates a connection with the MongoDB server and database
        """
        self.connection = MongoClient(self.server)
        self.database = self.connection[self.database_name]
        self.status = STATUS_CONNECTED

    def close(self):
        """
        Closes the connection to the MongoDB server
        """
        self.connection.close()
        self.status = STATUS_CLOSED

    def insert_document(self, object_name, document=None):
        """
        inserts a new document into the specified collection
        """
        if document is None:
            document = dict()
        self.database[object_name].insert(document)

    def get_document(self, object_name, query_filter=None):
        """
        Retrieves a document from the MongoDB database using the
        specified collection and query filter
        """
        if query_filter is None:
            query_filter = dict()
        document = self.database[object_name].find_one(query_filter)
        # remove the mongodb _id form the document
        if document:
            document.pop("_id")
        return document

    def get_documents(self, object_name, query_filter=None):
        """
        Retrieves multiple documents from the MongoDB database using the
        specified collection and query filter
        """
        if query_filter is None:
            query_filter = dict()
        documents = self.database[object_name].find(query_filter)
        # remove the mongodb _id form the document

        cleaned = []
        for doc in documents:
            doc.pop('_id', None)
            cleaned.append(doc)

        return cleaned

    def update_document(self, object_name, document, query_filter=None):
        """
        Updates an existing document that matches the query filter
        """
        if query_filter is None:
            query_filter = dict()

        self.database[object_name].update(
            query_filter, document)

    def delete_document(self, object_name, query_filter=None, limit_one=False):
        """
        deletes all documents that match the query filter
        """
        if query_filter is None:
            query_filter = dict()
        self.database[object_name].remove(query_filter, True)
