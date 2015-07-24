import uuid

from specter import expect, require, skip

from spec.rift.api.resources.fixtures import MockedDatabase
from spec.rift.api.datasets import VALID_SCHEDULES


class SchedulesResource(MockedDatabase):

    def before_each(self):
        super(type(self), self).before_each()
        post_resp = self._post_schedule()
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
        expect(resp.json['entries']).to.equal([])

    def can_head_schedule(self):
        resp = self.app.head(self.schedule_path)
        expect(resp.status_int).to.equal(200)

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

    def _post_schedule(self):
        body = VALID_SCHEDULES['schedule_with_empty_entries']['body']
        resp = self.app.post_json('/v1/user/schedules', body)
        require(resp.status_int).to.equal(201)
        require(resp.json).to.contain('schedule_id')
        return resp
