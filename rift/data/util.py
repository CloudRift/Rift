from rift.data.handler import get_handler
from rift.data.model import build_job_from_dict

JOB_COLLECTION = "jobs"


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

