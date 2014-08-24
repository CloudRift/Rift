from rift.data.models.target import Target
from uuid import uuid4


def create_target():
    source_dict = {
        "name": "Apache node 2",
        "type": "cloud-server",
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
    return Target.build_target_from_dict(str(uuid4()), source_dict)
