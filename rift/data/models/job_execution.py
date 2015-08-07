import uuid

from rift.data.handler import get_handler

JOB_RUN_COLLECTION = "job_execution"


class JobExecution(object):

    def __init__(self, tenant_id, job_id, run_number, status):
        self.tenant_id = tenant_id
        self.job_id = job_id
        self.run_number = run_number
        self.status = status

    def as_dict(self):
        return {
            "tenant_id": self.tenant_id,
            "id": self.job_id,
            "run_number": self.run_number,
            "status": self.status
        }

    @classmethod
    def build_job_from_dict(cls, job_dict):
        kwargs = {
            "tenant_id": job_dict.get("tenant_id"),
            "job_id": job_dict.get("id"),
            "run_number": job_dict.get("run_number", str(uuid.uuid4())),
            "status": job_dict.get("status", "in-progress")
        }
        return JobExecution(**kwargs)

    @classmethod
    def save_job(cls, job, handler=None):
        job_dict = job.as_dict()
        job_dict['tenant_id'] = job.tenant_id

        db_handler = handler or get_handler()
        db_handler.insert_document(
            object_name=JOB_RUN_COLLECTION, document=job_dict
        )

    @classmethod
    def update_job(cls, job, handler=None):
        db_handler = handler or get_handler()
        db_handler.update_document(
            object_name=JOB_RUN_COLLECTION,
            document=job.as_dict(),
            query_filter={"run_number": job.run_number}
        )

    @classmethod
    def get_job(cls, run_number, handler=None):
        db_handler = handler or get_handler()
        job_dict = db_handler.get_document(
            object_name=JOB_RUN_COLLECTION,
            query_filter={"run_number": run_number}
        )

        return JobExecution.build_job_from_dict(job_dict)

    @classmethod
    def delete_job(cls, run_number, handler=None):
        db_handler = handler or get_handler()
        db_handler.delete_document(
            object_name=JOB_RUN_COLLECTION,
            query_filter={"run_number": run_number}
        )
