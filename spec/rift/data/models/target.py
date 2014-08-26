import uuid
from specter import Spec, expect
from rift.data.models.target import Target
from spec.rift.data.common import create_target, example_target_dict


class TargetModel(Spec):
    class Serialization(Spec):
        def before_all(self):
            self.target = create_target()
            self.example_dict = example_target_dict()

        def can_serialize_to_a_dictionary(self):
            target_dict = self.target.as_dict()

            expect(target_dict['id']).to.equal(self.example_dict['id'])
            expect(target_dict['name']).to.equal(self.example_dict['name'])
            expect(target_dict['type']).to.equal(self.example_dict['type'])

        def can_serialize_to_a_summary_dictionary(self):
            summary_dict = self.target.summary_dict()

            expect(summary_dict['id']).to.equal(self.example_dict['id'])
            expect(summary_dict['name']).to.equal(self.example_dict['name'])
            expect(summary_dict['type']).to.equal(self.example_dict['type'])

    class Deserialization(Spec):
        def before_all(self):
            self.example_dict = example_target_dict()

        def can_deserialize_from_a_dictionary(self):
            tenant_id = str(uuid.uuid4())

            test_target = Target.build_target_from_dict(tenant_id,
                                                        self.example_dict)
            expect(test_target.id).to.equal(self.example_dict['id'])
            expect(test_target.name).to.equal(self.example_dict['name'])
            expect(test_target.target_type).to.equal(self.example_dict['type'])
