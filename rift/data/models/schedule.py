import uuid

from rift.data.handler import get_handler

SCHEDULE_COLLECTION = "schedules"


class Schedule(object):

    def __init__(self, tenant_id, schedule_id, entries, name):
        self.tenant_id = tenant_id
        self.schedule_id = schedule_id
        self.entries = entries
        self.name = name

    def as_dict(self):
        return {
            'id': self.schedule_id,
            'name': self.name,
            'entries': [e.as_dict() for e in self.entries],
        }

    @classmethod
    def build_schedule_from_dict(cls, tenant_id, schedule_dict):
        if not schedule_dict:
            return
        kwargs = {
            'schedule_id': schedule_dict.get('id', str(uuid.uuid4())),
            'name': schedule_dict.get('name'),
            'entries': [
                Entry.build_entry_from_dict(e)
                for e in schedule_dict.get('entries')
            ],
        }
        return cls(tenant_id, **kwargs)

    @classmethod
    def save_schedule(cls, schedule):
        db_dict = schedule.as_dict()
        db_dict['tenant_id'] = schedule.tenant_id

        db_handler = get_handler()
        db_handler.insert_document(
            object_name=SCHEDULE_COLLECTION, document=db_dict
        )

    @classmethod
    def get_schedule(cls, tenant_id, schedule_id):
        db_handler = get_handler()
        schedule_dict = db_handler.get_document(
            object_name=SCHEDULE_COLLECTION,
            query_filter={"id": schedule_id})
        return cls.build_schedule_from_dict(tenant_id, schedule_dict)

    @classmethod
    def get_schedules(cls, tenant_id):
        db_handler = get_handler()
        schedules_dict = db_handler.get_documents(
            object_name=SCHEDULE_COLLECTION,
            query_filter={"tenant_id": tenant_id})
        return [cls.build_schedule_from_dict(tenant_id, schedule)
                for schedule in schedules_dict]

    @classmethod
    def delete_schedule(cls, schedule_id):
        db_handler = get_handler()
        db_handler.delete_document(
            object_name=SCHEDULE_COLLECTION,
            query_filter={"id": schedule_id})


class Entry(object):

    def __init__(self, job_id, delay):
        self.job_id = job_id
        self.delay = delay

    def as_dict(self):
        return {
            'job_id': self.job_id,
            'delay': self.delay,
        }

    @classmethod
    def build_entry_from_dict(cls, entry_dict):
        kwargs = {
            'job_id': entry_dict.get('job_id'),
            'delay': entry_dict.get('delay'),
        }
        return cls(**kwargs)
