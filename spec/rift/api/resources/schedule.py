import json
import uuid

from specter import DataSpec, expect, require, skip
import mock

from spec.rift.api.resources.fixtures import MockedDatabase
from spec.rift.api.datasets import VALID_SCHEDULES, INVALID_SCHEDULES


class SchedulesResource(MockedDatabase):

    def before_each(self):
        super(type(self), self).before_each()
        body = VALID_SCHEDULES['schedule_with_one_entry']['body']
        self.schedule_body = json.loads(body)
        post_resp = self._post_schedule(self.schedule_body)
        self.schedule_id = post_resp.json['schedule_id']
        self.schedule_path = '/v1/user/schedules/{0}'.format(self.schedule_id)

    def can_list_schedules(self):
        resp = self.app.get('/v1/user/schedules')
        require(resp.status_int).to.equal(200)
        require(resp.json).to.contain('schedules')
        expect(len(resp.json['schedules'])).to.equal(1)

    def can_get_schedule(self):
        resp = self.app.get(self.schedule_path)
        require(resp.status_int).to.equal(200)
        expect(resp.json).to.contain('id')
        expect(resp.json).to.contain('name')

        require(resp.json).to.contain('entries')
        expect(len(resp.json['entries'])).to.equal(1)
        expect(resp.json['entries'][0]).to.contain('job_id')
        expect(resp.json['entries'][0]).to.contain('delay')

    @skip('Fails - "not enough arguments for format string" in mongomock')
    def can_delete_schedule(self):
        resp = self.app.delete(self.schedule_path)
        require(resp.status_int).to.equal(200)

        resp = self.app.get(self.schedule_path, expect_errors=True)
        expect(resp.status_int).to.equal(404)

    def get_404s_on_missing_schedule(self):
        resp = self.app.get('/v1/user/schedules/{0}'.format(uuid.uuid4()),
                            expect_errors=True)
        expect(resp.status_int).to.equal(404)

    def head_404s_on_missing_schedule(self):
        resp = self.app.head('/v1/user/schedules/{0}'.format(uuid.uuid4()),
                             expect_errors=True)
        expect(resp.status_int).to.equal(404)

    def _post_schedule(self, body):
        resp = self.app.post_json('/v1/user/schedules', body)
        require(resp.status_int).to.equal(201)
        require(resp.json).to.contain('schedule_id')
        return resp

    class SuccessfulPostRequests(MockedDatabase, DataSpec):
        DATASET = VALID_SCHEDULES

        def can_post_self(self, body):
            body = json.loads(body)
            resp = self.app.post_json('/v1/user/schedules', body)
            require(resp.status_int).to.equal(201)
            expect(resp.json).to.contain('schedule_id')

    class BadPostRequests(MockedDatabase, DataSpec):
        DATASET = INVALID_SCHEDULES

        def returns_400_on_a(self, body):
            body = json.loads(body)
            resp = self.app.post_json('/v1/user/schedules', body,
                                      expect_errors=True)
            expect(resp.status_int).to.equal(400)

    class SuccessfulHeadRequests(MockedDatabase, DataSpec):
        DATASET = VALID_SCHEDULES

        def can_run_schedule(self, body):
            schedule_body = json.loads(body)

            # post a schedule
            post_resp = self.app.post_json('/v1/user/schedules', schedule_body)
            require(post_resp.status_int).to.equal(201)
            require(post_resp.json).to.contain('schedule_id')
            schedule_id = post_resp.json['schedule_id']
            schedule_path = '/v1/user/schedules/{0}'.format(schedule_id)

            # run the schedule
            with mock.patch('rift.api.resources.execute_job') as execute_job:
                resp = self.app.head(schedule_path)
                expect(resp.status_int).to.equal(200)
                n_entries = len(schedule_body['entries'])
                expect(len(execute_job.mock_calls)).to.equal(n_entries)
