import uuid
from specter import Spec, expect
from rift.data.models.target import Target
from spec.rift.data.common import create_target


class TargetModel(Spec):
    def can_convert_to_dictionary(self):
        target = create_target()
        target_dict = target.as_dict()

        tenant_id = str(uuid.uuid4())
        test_dict = Target.build_target_from_dict(
            tenant_id, target_dict).as_dict()
        expect(target_dict).to.equal(test_dict)
