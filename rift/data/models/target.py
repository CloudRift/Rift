import uuid
from rift.data.handler import get_handler
from rift.data.models.address import Address

TARGET_COLLECTION = "targets"


class Target(object):
    """
    Represents a target node to execute actions against
    """
    def __init__(self, tenant_id, target_type, address, authentication,
                 target_id, name=None):
        self.tenant_id = tenant_id
        self.target_type = target_type
        self.address = address
        self.authentication = authentication
        self.name = name
        self.id = target_id

    def as_dict(self):
        return {
            'id': self.id,
            'type': self.target_type,
            'name': self.name,
            'address': self.address.as_dict(),
            'authentication': self.authentication
        }

    def summary_dict(self):
        """ Used for more efficient display of collections """
        return {
            'id': self.id,
            'name': self.name,
            'type': self.target_type,
        }

    @classmethod
    def build_target_from_dict(cls, tenant_id, target_dict):
        if not target_dict:
            return

        address_obj = Address.build_from_dict(target_dict.get('address'))

        kwargs = {
            'target_id': target_dict.get('id', str(uuid.uuid4())),
            'target_type': target_dict.get('type'),
            'address': address_obj,
            'authentication': target_dict.get('authentication'),
            'name': target_dict.get('name')
        }
        return Target(tenant_id, **kwargs)

    @classmethod
    def save_target(cls, target):
        db_dict = target.as_dict()
        db_dict['tenant_id'] = target.tenant_id

        db_handler = get_handler()
        db_handler.insert_document(
            object_name=TARGET_COLLECTION, document=db_dict
        )

    @classmethod
    def get_target(cls, tenant_id, target_id):
        db_handler = get_handler()
        target_dict = db_handler.get_document(
            object_name=TARGET_COLLECTION,
            query_filter={"id": target_id})

        return Target.build_target_from_dict(tenant_id, target_dict)

    @classmethod
    def get_targets(cls, tenant_id):
        db_handler = get_handler()
        targets_dict = db_handler.get_documents(
            object_name=TARGET_COLLECTION,
            query_filter={"tenant_id": tenant_id})

        return [Target.build_target_from_dict(tenant_id, target)
                for target in targets_dict]
