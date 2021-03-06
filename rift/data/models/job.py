import uuid

from rift.data.models.action import Action
from rift.data.handler import get_handler

JOB_COLLECTION = "jobs"


class Job(object):
    def __init__(self, tenant_id, job_id, name, actions, run_numbers=None):
        self.tenant_id = tenant_id
        self.name = name
        if run_numbers is None:
            self.run_numbers = list()
        else:
            self.run_numbers = run_numbers
        self.actions = actions
        self.id = job_id

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "actions": [action.as_dict() for action in self.actions],
            "run_numbers": self.run_numbers,
        }

    def summary_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def build_job_from_dict(cls, job_dict):
        actions = []
        for action in job_dict.get("actions", []):
            actions.append(Action.build_action_from_dict(action))

        kwargs = {
            'tenant_id': job_dict.get("tenant_id"),
            'job_id': job_dict.get("id", str(uuid.uuid4())),
            'name': job_dict.get("name"),
            'actions': actions,
            'run_numbers': job_dict.get("run_numbers")
        }

        return Job(**kwargs)

    @classmethod
    def save_job(cls, job, handler=None):
        job_dict = job.as_dict()
        job_dict['tenant_id'] = job.tenant_id

        db_handler = handler or get_handler()
        db_handler.insert_document(
            object_name=JOB_COLLECTION, document=job_dict
        )

    @classmethod
    def update_job(cls, job, handler=None):
        db_handler = handler or get_handler()
        db_handler.update_document(
            object_name=JOB_COLLECTION,
            document=job.as_dict(),
            query_filter={"id": job.id}
        )

    @classmethod
    def get_job(cls, job_id, handler=None):
        db_handler = handler or get_handler()
        job_dict = db_handler.get_document(
            object_name=JOB_COLLECTION,
            query_filter={"id": job_id})

        return Job.build_job_from_dict(job_dict)

    @classmethod
    def get_jobs(cls, tenant_id, handler=None):
        db_handler = handler or get_handler()
        jobs_dict = db_handler.get_documents(
            object_name=JOB_COLLECTION,
            query_filter={"tenant_id": tenant_id})

        return [Job.build_job_from_dict(job) for job in jobs_dict]

    @classmethod
    def delete_job(cls, job_id, handler=None):
        db_handler = handler or get_handler()
        db_handler.delete_document(
            object_name=JOB_COLLECTION,
            query_filter={"id": job_id}
        )
