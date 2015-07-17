import json

from specter import DataSpec, expect, require

from spec.rift.api.resources.fixtures import MockedDatabase
import spec.rift.api.schemas.job
from spec.rift.api.datasets import INVALID_JOBS, VALID_JOBS


class JobsResource(MockedDatabase):

    def can_list_jobs(self):
        resp = self.app.get('/v1/tenant/jobs')
        require(resp.status_int).to.equal(200)
        require(resp.json).to.contain('jobs')
        expect(resp.json['jobs']).to.equal([])

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
