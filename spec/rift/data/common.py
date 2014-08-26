from pretend import stub, call_recorder
from uuid import uuid4

from rift.data.models.target import Target


def example_target_dict():
    return {
        "name": "Apache node 2",
        "type": "cloud-server",
        "id": "1234",
        "address": {
            "nova": {
                "name": "apache-02.ord.dev",
                "region": "DFW"
                }
        },
        "authentication": {
            "rackspace": {
                "username": "your_username",
                "api_key": "your_api_key"
            }
        }
    }


def create_target():
    return Target.build_target_from_dict(str(uuid4()), example_target_dict())


def create_db_handler_stub(insert_rtn=None, update_rtn=None, delete_rtn=None,
                           get_rtn=None, gets_rtn=None):
    update_document = lambda object_name, document, query_filter: update_rtn
    insert_document = lambda object_name, document: insert_rtn
    delete_document = lambda object_name, query_filter: delete_rtn
    get_documents = lambda object_name, query_filter: gets_rtn
    get_document = lambda object_name, query_filter: get_rtn

    handler = stub(
        insert_document=call_recorder(insert_document),
        update_document=call_recorder(update_document),
        get_document=call_recorder(get_document),
        get_documents=call_recorder(get_documents),
        delete_document=call_recorder(delete_document)
    )
    return handler
