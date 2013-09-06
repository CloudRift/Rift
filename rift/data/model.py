class Tenant(object):
    def __init__(self, tenant_id, name=None, targets=None):
        self.tenant_id = tenant_id
        self.name = name
        self.targets = targets if targets is not None else list()

    def as_dict(self):
        pass


class Target(object):
    def __init__(self):
        pass

    def as_dict(self):
        pass


class Job(object):
    def __init__(self):
        pass

    def as_dict(self):
        pass


class Action(object):
    def __init__(self):
        pass

    def as_dict(self):
        pass


