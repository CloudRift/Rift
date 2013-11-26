import uuid

from rift.data.handler import get_handler

JOB_COLLECTION = "jobs"
TENANT_COLLECTION = "tenants"


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
    def __init__(self, targets, action_type, parameters=None):
        self.targets = targets
        self.action_type = action_type
        self.parameters = parameters if parameters is not None else dict()

    def as_dict(self):
        return {
            "targets": [target.as_dict() for target in self.targets],
            "action_type": self.action_type,
            "parameters": self.parameters
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
    tenant_id = job_dict["tenant_id"]
    name = job_dict["name"]
    actions = [
        _build_action_from_dict(action_dict)
        for action_dict in job_dict["actions"]]
    job_id = job_dict["job_id"]

    return Job(tenant_id=tenant_id, name=name, actions=actions, job_id=job_id)


def _build_action_from_dict(action_dict):
    targets = [
        _build_target_from_dict(target_dict)
        for target_dict in action_dict["targets"]]
    action_type = action_dict["action_type"]
    parameters = action_dict["parameters"]
    return Action(
        targets=targets,
        action_type=action_type,
        parameters=parameters
    )


def _build_target_from_dict(target_dict):
    return Target(**target_dict)


def save_job(job):
    db_handler = get_handler()
    db_handler.insert_document(
        object_name=JOB_COLLECTION, document=job.as_dict()
    )


def update_job(job):
    db_handler = get_handler()
    db_handler.update_document(
        object_name=JOB_COLLECTION,
        document=job.as_dict(),
        query_filter={"job_id": job.job_id}
    )

def get_job(job_id):
    db_handler = get_handler()
    job_dict = db_handler.get_document(
        object_name=JOB_COLLECTION,
        query_filter={"job_id": job_id})

    return build_job_from_dict(job_dict)

def get_jobs(tenant_id):
    db_handler = get_handler()
    jobs_dict = db_handler.get_documents(
        object_name=JOB_COLLECTION,
        query_filter={"tenant_id": tenant_id})

    return [build_job_from_dict(job) for job in jobs_dict]

def delete_job(job_id):
    db_handler = get_handler()
    db_handler.delete_document(
        object_name=JOB_COLLECTION,
        query_filter={"job_id": job_id}
    )


def build_tenant_from_dict(tenant_dict):
    tenant_id = tenant_dict["tenant_id"]
    name = tenant_dict["name"]
    targets = [
        _build_target_from_dict(target_dict)
        for target_dict in tenant_dict["targets"]]
    return Tenant(tenant_id=tenant_id, name=name, targets=targets)


def save_tenant(tenant):
    db_handler = get_handler()
    db_handler.insert_document(
        object_name=TENANT_COLLECTION, document=tenant.as_dict()
    )


def get_tenant(tenant_id):
    db_handler = get_handler()
    tenant_dict = db_handler.get_document(
        object_name=TENANT_COLLECTION,
        query_filter={"tenant_id": tenant_id})

    return build_tenant_from_dict(tenant_dict)


def update_tenant(tenant):
    db_handler = get_handler()
    db_handler.update_document(
        object_name=TENANT_COLLECTION,
        document=tenant.as_dict(),
        query_filter={"tenant_id": tenant.tenant_id}
    )
