from specter import Spec, expect

from rift.data.models.job import Job
from rift.data.models.action import Action
from spec.rift.data.common import create_target, create_db_handler_stub


example_job_dict = {
    'tenant_id': '123',
    'id': '1001',
    'name': 'Soft and then hard reboot db servers',
    'actions': [
        {
            'targets': ['83a57a53-4a50-42e5-acb4-dc301736062a'],
            'type': 'nova-soft-reboot'
        }
    ]
}


class JobModel(Spec):
    class Serialization(Spec):
        def before_all(self):
            target = create_target()
            self.targets = [target]

            action = Action(targets=self.targets, action_type='soft-reboot')
            self.actions = [action]

            self.job = Job(
                tenant_id='123',
                name='do_stuff',
                actions=self.actions,
                job_id='12345'
            )

        def can_serialize_to_a_dictionary(self):
            job_dict = self.job.as_dict()
            action_dict = self.actions[0].as_dict()

            expect(job_dict['id']).to.equal(self.job.id)
            expect(job_dict['name']).to.equal(self.job.name)
            expect(job_dict['actions']).to.equal([action_dict])

        def can_serialize_to_a_summary_dictionary(self):
            job_dict = self.job.summary_dict()

            expect(job_dict['id']).to.equal(self.job.id)
            expect(job_dict['name']).to.equal(self.job.name)

    class Deserialization(Spec):
        def before_all(self):
            self.job_dict = example_job_dict

        def can_deserialize_from_a_dictionary(self):
            job = Job.build_job_from_dict(self.job_dict)
            test_action_type = self.job_dict['actions'][0]['type']

            expect(job.id).to.equal(self.job_dict['id'])
            expect(job.name).to.equal(self.job_dict['name'])
            expect(job.actions[0].action_type).to.equal(test_action_type)

    class DatabaseActions(Spec):
        def before_all(self):
            self.job_dict = example_job_dict
            self.job = Job.build_job_from_dict(self.job_dict)

        def before_each(self):
            self.handler = create_db_handler_stub(
                get_rtn=self.job_dict,
                gets_rtn=[self.job_dict]
            )

        def can_save(self):
            Job.save_job(self.job, handler=self.handler)
            expect(len(self.handler.insert_document.calls)).to.equal(1)

        def can_update(self):
            Job.update_job(self.job, handler=self.handler)
            expect(len(self.handler.update_document.calls)).to.equal(1)

        def can_get_a_job(self):
            retrieved_job = Job.get_job(self.job.id, handler=self.handler)

            expect(len(self.handler.get_document.calls)).to.equal(1)
            expect(retrieved_job.id).to.equal(self.job.id)

        def can_get_jobs(self):
            tenant_id = self.job.tenant_id
            retrieved_jobs = Job.get_jobs(tenant_id, handler=self.handler)

            expect(len(self.handler.get_documents.calls)).to.equal(1)
            expect(len(retrieved_jobs)).to.equal(1)

        def can_delete(self):
            Job.delete_job(self.job.id, handler=self.handler)
            expect(len(self.handler.delete_document.calls)).to.equal(1)
