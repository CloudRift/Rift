import uuid

from specter import Spec, expect, skip

from rift.data.models.schedule import Schedule, Entry, Delay
from spec.rift.api.resources.fixtures import MockedDatabase


example_schedule_dict = {
    'id': '1234',
    'name': 'my schedule',
    'entries': [
        {
            "job_id": "job1",
            "delay": {
                "seconds": 3,
                "minutes": 2,
                "hours": 1,
            }
        }
    ]
}


class ScheduleModel(Spec):

    class Deserialization(Spec):
        def can_deserialize_from_a_dictionary(self):
            tenant_id = str(uuid.uuid4())
            schedule = Schedule.build_schedule_from_dict(
                tenant_id, example_schedule_dict)

            expect(schedule.tenant_id).to.equal(tenant_id)
            expect(schedule.schedule_id).to.equal('1234')
            expect(schedule.name).to.equal('my schedule')

            expect(schedule.entries[0].job_id).to.equal('job1')
            expect(schedule.entries[0].delay.seconds).to.equal(3)
            expect(schedule.entries[0].delay.minutes).to.equal(2)
            expect(schedule.entries[0].delay.hours).to.equal(1)

    class Serialization(Spec):
        def can_serialize_to_a_dictionary(self):
            delay = Delay(seconds=1, minutes=2, hours=3)
            entry = Entry(job_id='job1', delay=delay)
            schedule = Schedule(tenant_id='tenant1',
                                schedule_id='schedule1',
                                entries=[entry],
                                name='my schedule')

            schedule_dict = schedule.as_dict()
            expect(schedule_dict.get('id')).to.equal('schedule1')
            expect(schedule_dict.get('name')).to.equal('my schedule')
            expect(len(schedule_dict.get('entries', []))).to.equal(1)

            e = schedule_dict['entries'][0]
            expect(e.get('job_id')).to.equal('job1')
            expect(e.get('delay')).to.equal({
                'seconds': 1,
                'minutes': 2,
                'hours': 3,
            })

    class DatabaseActions(MockedDatabase):
        def before_each(self):
            super(type(self), self).before_each()
            self.tenant_id = str(uuid.uuid4())
            self.schedule = Schedule.build_schedule_from_dict(
                self.tenant_id, example_schedule_dict)
            Schedule.save_schedule(self.schedule)

        def can_save_and_get_a_schedule(self):
            found = Schedule.get_schedule(
                self.tenant_id, self.schedule.schedule_id)
            expect(found.as_dict()).to.equal(example_schedule_dict)

        def should_fail_to_get_missing_schedule(self):
            found = Schedule.get_schedule(self.tenant_id, str(uuid.uuid4()))
            expect(found).to.be_none()

        def can_get_schedules(self):
            schedules = Schedule.get_schedules(self.tenant_id)
            expect(len(schedules)).to.equal(1)
            expect(schedules[0].as_dict()).to.equal(example_schedule_dict)

        @skip('Fails - "not enough arguments for format string" in mongomock')
        def can_delete(self):
            Schedule.delete_schedule(self.schedule.schedule_id)
            found = Schedule.get_schedule(
                self.tenant_id, self.schedule.schedule_id)
            expect(found).to.be_none()

    class DelayModel(Spec):

        def can_get_total_seconds(self):
            delay = Delay(seconds=3, minutes=2, hours=1)
            expect(delay.get_total_seconds()).to.equal(3723)
