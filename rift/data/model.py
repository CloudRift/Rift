import uuid

from rift.data.handler import get_handler

JOB_COLLECTION = "jobs"
TENANT_COLLECTION = "tenants"
TARGET_COLLECTION = "targets"


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

    @classmethod
    def build_tenant_from_dict(cls, tenant_dict):
        tenant_id = tenant_dict.get("tenant_id")
        name = tenant_dict.get("name")
        targets = [
            Target.build_target_from_dict(target_dict)
            for target_dict in tenant_dict.get("targets")]
        return Tenant(tenant_id=tenant_id, name=name, targets=targets)

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

        tenant = Tenant.build_tenant_from_dict(tenant_dict)

        # Create Tenant if it doesn't exist
        if not tenant_dict:
            tenant = cls(tenant_id)
            cls.save_tenant(tenant)

        return tenant

    @classmethod
    def update_tenant(cls, tenant):
        db_handler = get_handler()
        db_handler.update_document(
            object_name=TENANT_COLLECTION,
            document=tenant.as_dict(),
            query_filter={"tenant_id": tenant.tenant_id}
        )


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

    @classmethod
    def build_job_from_dict(cls, job_dict):
        tenant_id = job_dict.get("tenant_id")
        name = job_dict.get("name")
        actions = [
            Action.build_action_from_dict(action_dict)
            for action_dict in job_dict.get("actions")]
        job_id = job_dict.get("job_id")

        return Job(tenant_id=tenant_id, name=name, actions=actions,
                   job_id=job_id)

    @classmethod
    def save_job(cls, job):
        db_handler = get_handler()
        db_handler.insert_document(
            object_name=JOB_COLLECTION, document=job.as_dict()
        )

    @classmethod
    def update_job(cls, job):
        db_handler = get_handler()
        db_handler.update_document(
            object_name=JOB_COLLECTION,
            document=job.as_dict(),
            query_filter={"job_id": job.job_id}
        )

    @classmethod
    def get_job(cls, job_id):
        db_handler = get_handler()
        job_dict = db_handler.get_document(
            object_name=JOB_COLLECTION,
            query_filter={"job_id": job_id})

        return Job.build_job_from_dict(job_dict)

    @classmethod
    def get_jobs(cls, tenant_id):
        db_handler = get_handler()
        jobs_dict = db_handler.get_documents(
            object_name=JOB_COLLECTION,
            query_filter={"tenant_id": tenant_id})

        return [Job.build_job_from_dict(job) for job in jobs_dict]

    @classmethod
    def delete_job(cls, job_id):
        db_handler = get_handler()
        db_handler.delete_document(
            object_name=JOB_COLLECTION,
            query_filter={"job_id": job_id}
        )


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

    @classmethod
    def build_action_from_dict(cls, action_dict):
        targets = [
            Target.build_target_from_dict(target_dict)
            for target_dict in action_dict.get("targets")]
        action_type = action_dict.get("action_type")
        parameters = action_dict.get("parameters")
        return Action(
            targets=targets,
            action_type=action_type,
            parameters=parameters
        )


class Target(object):
    """
    Represents a target node to execute actions against
    """
    def __init__(self, tenant_id, target_type, address, address_type,
                 authentication, name=None, target_id=None):
        self.tenant_id = tenant_id
        self.target_type = target_type
        self.address = address
        self.address_type = address_type
        self.authentication = authentication
        self.name = name
        self.target_id = target_id if target_id else str(uuid.uuid4())

    def db_dict(self):
        converted = self.as_dict()
        converted['tenant_id'] = self.tenant_id

        return converted

    def as_dict(self):
        return {
            "target_id": self.target_id,
            "target_type": self.target_type,
            "address": self.address,
            "address_type": self.address_type,
            "authentication": self.authentication,
            "name": self.name
        }

    @classmethod
    def build_target_from_dict(cls, tenant_id, target_dict):
        if not target_dict:
            return

        kwargs = {
            'target_type': target_dict.get('type'),
            'address': target_dict.get('address'),
            'address_type': target_dict.get('address_type'),
            'authentication': target_dict.get('authentication'),
            'name': target_dict.get('name')
        }
        return Target(tenant_id, **kwargs)

    @classmethod
    def save_target(cls, target):
        db_handler = get_handler()
        db_handler.insert_document(
            object_name=TARGET_COLLECTION, document=target.db_dict()
        )

    @classmethod
    def get_target(cls, tenant_id, target_id):
        db_handler = get_handler()
        target_dict = db_handler.get_document(
            object_name=TARGET_COLLECTION,
            query_filter={"target_id": target_id})

        return Target.build_target_from_dict(tenant_id, target_dict)

    @classmethod
    def get_targets(cls, tenant_id):
        db_handler = get_handler()
        targets_dict = db_handler.get_documents(
            object_name=TARGET_COLLECTION,
            query_filter={"tenant_id": tenant_id})

        return [Target.build_target_from_dict(tenant_id, target)
                for target in targets_dict]
