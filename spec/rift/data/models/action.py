import uuid

from specter import Spec, expect
from rift.data.models.action import Action
from spec.rift.data.common import create_target


class ActionModel(Spec):

    class Serialization(Spec):
        def before_all(self):
            self.example_target = create_target()
            self.example_action = Action(targets=[self.example_target],
                                         action_type='soft-reboot')

        def can_serialize_to_a_dictionary(self):
            action_dict = self.example_action.as_dict()

            expect(action_dict['type']).to.equal('soft-reboot')

    class Deserialization(Spec):
        def before_all(self):

            self.example = {
                'type': 'soft-reboot',
                'targets': [str(uuid.uuid4())]
            }

        def can_deserialize_from_a_dictionary(self):
            action = Action.build_action_from_dict(self.example)

            expect(action.action_type).to.equal(self.example['type'])
            expect(action.targets[0]).to.equal(self.example['targets'][0])
