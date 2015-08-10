import json
from mock import patch
import uuid

from specter import DataSpec, expect, require, skip

from spec.rift.api.resources.fixtures import MockedDatabase
from spec.rift.api.datasets import INVALID_JOBS, VALID_JOBS


class JobsResource(MockedDatabase):

    def can_list_jobs(self):
        resp = self.app.get('/v1/tenant/jobs')
        require(resp.status_int).to.equal(200)
        require(resp.json).to.contain('jobs')
        expect(resp.json['jobs']).to.equal([])

    def can_get_job(self):
        post_resp = self._post_job()
        job_id = post_resp.json['job_id']

        resp = self.app.get('/v1/tenant/jobs/{0}'.format(job_id))
        require(resp.status_int).to.equal(200)
        expect(resp.json).to.contain('id')
        expect(resp.json).to.contain('actions')
        expect(resp.json).to.contain('name')
        expect(resp.json['id']).to.equal(job_id)

    @patch('rift.actions.execute_job.delay')
    def can_get_job_status(self, execute_job):
        post_resp = self._post_job()
        job_id = post_resp.json['job_id']

        self.app.head('/v1/tenant/jobs/{0}'.format(job_id))

        job_resp = self.app.get('/v1/tenant/jobs/{0}'.format(job_id))
        run_number = job_resp.json['run_numbers'][0]

        resp = self.app.get('/v1/tenant/jobs/{0}/history/{1}'
                            ''.format(job_id, run_number))

        expect(resp.json).to.contain('id')
        expect(resp.json).to.contain('run_number')
        expect(resp.json).to.contain('status')

    @skip('Fails - "not enough arguments for format string" in mongomock')
    def can_delete_job(self):
        post_resp = self._post_job()
        job_id = post_resp.json['job_id']

        resp = self.app.delete('/v1/tenant/jobs/{0}'.format(job_id),
                               expect_errors=True)
        expect(resp.status_int).to.equal(200)

    @skip('Fails - internal server error')
    def should_404_on_nonexistent_job(self):
        resp = self.app.get('/v1/tenant/jobs/{0}'.format(uuid.uuid4()),
                            expect_errors=True)
        expect(resp.status_int).to.equal(404)

    def _post_job(self):
        body = json.loads(VALID_JOBS['job_with_empty_actions']['body'])
        post_resp = self.app.post_json('/v1/tenant/jobs', body)
        require(post_resp.status_int).to.equal(201)
        require(post_resp.json).to.contain('job_id')
        return post_resp

    class SuccessfulPostRequests(MockedDatabase, DataSpec):
        DATASET = VALID_JOBS

        def can_post(self, body):
            body = json.loads(body)
            resp = self.app.post_json('/v1/tenant/jobs', body)
            require(resp.status_int).to.equal(201)
            expect(resp.json).to.contain('job_id')

    class BadPostRequests(MockedDatabase, DataSpec):
        DATASET = INVALID_JOBS

        def returns_400_on_a(self, body):
            body = json.loads(body)
            resp = self.app.post_json('/v1/tenant/jobs', body,
                                      expect_errors=True)
            expect(resp.status_int).to.equal(400)
