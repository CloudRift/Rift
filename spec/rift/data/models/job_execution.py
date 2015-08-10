from specter import Spec, expect

from rift.data.models.job_execution import JobExecution
from spec.rift.data.common import create_db_handler_stub


example_job_dict = {
    'tenant_id': '123',
    'id': '1001',
    'run_number': '2012',
    'status': 'in-progress',
}


class JobExecutionModel(Spec):
    class Serialization(Spec):
        def before_all(self):
            self.job_ex = JobExecution(
                tenant_id='123',
                job_id='1001',
                run_number='2012',
                status='in-progress'
            )

        def can_serialize_to_a_dictionary(self):
            job_dict = self.job_ex.as_dict()

            expect(job_dict['id']).to.equal(self.job_ex.job_id)
            expect(job_dict['tenant_id']).to.equal(self.job_ex.tenant_id)
            expect(job_dict['run_number']).to.equal(self.job_ex.run_number)
            expect(job_dict['status']).to.equal(self.job_ex.status)

    class Deserialization(Spec):
        def before_all(self):
            self.job_dict = example_job_dict

        def can_deserialize_from_a_dictionary(self):
            job_ex = JobExecution.build_job_from_dict(self.job_dict)

            expect(job_ex.job_id).to.equal(self.job_dict['id'])
            expect(job_ex.tenant_id).to.equal(self.job_dict['tenant_id'])
            expect(job_ex.run_number).to.equal(self.job_dict['run_number'])
            expect(job_ex.status).to.equal('in-progress')

    class DatabaseActions(Spec):
        def before_all(self):
            self.job_dict = example_job_dict
            self.job_ex = JobExecution.build_job_from_dict(self.job_dict)

        def before_each(self):
            self.handler = create_db_handler_stub(
                get_rtn=self.job_dict,
                gets_rtn=[self.job_dict]
            )

        def can_save(self):
            JobExecution.save_job(self.job_ex, handler=self.handler)
            expect(len(self.handler.insert_document.calls)).to.equal(1)

        def can_update(self):
            JobExecution.update_job(self.job_ex, handler=self.handler)
            expect(len(self.handler.update_document.calls)).to.equal(1)

        def can_get_a_job_execution(self):
            retrieved_job = JobExecution.get_job(self.job_ex.run_number,
                                                 handler=self.handler)

            expect(len(self.handler.get_document.calls)).to.equal(1)
            expect(retrieved_job.run_number).to.equal(self.job_ex.run_number)

        def can_delete(self):
            JobExecution.delete_job(self.job_ex.run_number,
                                    handler=self.handler)
            expect(len(self.handler.delete_document.calls)).to.equal(1)
