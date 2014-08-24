from specter import Spec, expect
from rift.data.models.action import Action
from spec.rift.data.common import create_target


class ActionModel(Spec):
    def can_convert_to_dictionary(self):
        target1 = create_target()
        target2 = create_target()
        targets = [target1, target2]
        action = Action(targets=targets, action_type="soft-reboot")
        action_dict = action.as_dict()

        test_dict = Action.build_action_from_dict(action_dict).as_dict()
        expect(action_dict).to.equal(test_dict)
