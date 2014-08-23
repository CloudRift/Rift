class Action(object):
    def __init__(self, targets, action_type, parameters=None):
        self.targets = targets
        self.action_type = action_type
        self.parameters = parameters if parameters is not None else dict()

    def as_dict(self):
        return {
            "targets": self.targets,
            "type": self.action_type,
            "parameters": self.parameters
        }

    @classmethod
    def build_action_from_dict(cls, action_dict):
        kwargs = {
            'targets': action_dict.get("targets"),
            'action_type': action_dict.get("type"),
            'parameters': action_dict.get("parameters")
        }

        return Action(**kwargs)
