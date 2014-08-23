from rift.data.handler import get_handler
from rift import log

LOG = log.get_logger()
TENANT_COLLECTION = "tenants"


class Tenant(object):
    def __init__(self, tenant_id, name=None):
        self.tenant_id = tenant_id
        self.name = name

    def as_dict(self):
        return {
            "tenant_id": self.tenant_id,
            "name": self.name,
        }

    @classmethod
    def build_tenant_from_dict(cls, tenant_dict):
        kwargs = {
            'tenant_id': tenant_dict.get("tenant_id"),
            'name': tenant_dict.get("name")
        }
        return Tenant(**kwargs)

    @classmethod
    def save_tenant(cls, tenant):
        db_handler = get_handler()
        db_handler.insert_document(
            object_name=TENANT_COLLECTION, document=tenant.as_dict()
        )

    @classmethod
    def get_tenant(cls, tenant_id):
        db_handler = get_handler()
        tenant_dict = db_handler.get_document(
            object_name=TENANT_COLLECTION,
            query_filter={"tenant_id": tenant_id})

        # Create Tenant if it doesn't exist
        if not tenant_dict:
            LOG.info('Tenant {0} not found. Creating...'.format(tenant_id))
            tenant = cls(tenant_id)
            cls.save_tenant(tenant)
        else:
            tenant = Tenant.build_tenant_from_dict(tenant_dict)

        return tenant

    @classmethod
    def update_tenant(cls, tenant):
        db_handler = get_handler()
        db_handler.update_document(
            object_name=TENANT_COLLECTION,
            document=tenant.as_dict(),
            query_filter={"tenant_id": tenant.tenant_id}
        )
