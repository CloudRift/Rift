import uuid

from specter import Spec, expect
from rift.data.models.tenant import Tenant


class TenantModel(Spec):
    def can_convert_to_dictionary(self):
        tmp_uuid = str(uuid.uuid4())
        tenant = Tenant(name=tmp_uuid, tenant_id=tmp_uuid)
        tenant_dict = tenant.as_dict()

        test_dict = Tenant.build_tenant_from_dict(tenant_dict).as_dict()
        expect(tenant_dict).to.equal(test_dict)
