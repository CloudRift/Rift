import uuid


class Tenant(object):
    def __init__(self, tenant_id, name=None, targets=None):
        self.tenant_id = tenant_id
        self.name = name
        self.targets = targets if targets is not None else list()

    def as_dict(self):
        return {
            "tenant_id": self.tenant_id,
            "name": self.name,
            "targets": [target.as_dict() for target in self.targets]
        }


class Job(object):
    def __init__(self, tenant_id, name, actions, job_id=None):
        self.tenant_id = tenant_id
        self.name = name
        self.actions = actions
        self.job_id = job_id if job_id is not None else uuid.uuid4()

    def as_dict(self):
        return {
            "job_id": self.job_id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "actions": [action.as_dict() for action in self.actions]
        }


class Action(object):
    def __init__(self, targets, action_type):
        self.targets = targets
        self.action_type = action_type

    def as_dict(self):
        return {
            "targets": [target.as_dict() for target in self.targets],
            "action_type": self.action_type
        }


class Target(object):
    """
    Represents a target node to execute actions against
    """
    def __init__(self, name, public_ip, private_ip):
        self.name = name
        self.public_ip = public_ip
        self.private_ip = private_ip

    def as_dict(self):
        return {
            "name": self.name,
            "public_ip": self.public_ip,
            "private_ip": self.private_ip
        }

def build_job_from_dict(job_dict):
    pass


def build_action_from_dict(action_dict):
    pass
