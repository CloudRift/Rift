import uuid

from specter import expect, require, skip

from spec.rift.api.resources.fixtures import MockedDatabase
from spec.rift.api.datasets import VALID_SCHEDULES


class SchedulesResource(MockedDatabase):

    def can_list_schedules(self):
        resp = self.app.get('/v1/tenant/schedules')
        require(resp.status_int).to.equal(200)
        require(resp.json).to.contain('schedules')
        expect(resp.json['schedules']).to.equal([])

    def can_get_schedule(self):
        post_resp = self._post_schedule()
        schedule_id = post_resp.json['schedule_id']

        resp = self.app.get('/v1/tenant/schedules/{0}'.format(schedule_id))
        require(resp.status_int).to.equal(200)
        expect(resp.json).to.contain('id')
        expect(resp.json).to.contain('name')
        require(resp.json).to.contain('entries')
        expect(resp.json['entries']).to.equal([])

    @skip('Fails - "not enough arguments for format string" in mongomock')
    def can_delete_schedule(self):
        post_resp = self._post_schedule()
        schedule_id = post_resp.json['schedule_id']

        url = '/v1/tenant/schedules/{0}'.format(schedule_id)
        resp = self.app.delete(url)
        require(resp.status_int).to.equal(200)

        resp = self.app.get(url, expect_errors=True)
        expect(resp.status_int).to.equal(404)

    def should_404_on_nonexistent_schedule(self):
        resp = self.app.get('/v1/tenant/schedules/{0}'.format(uuid.uuid4()),
                            expect_errors=True)
        expect(resp.status_int).to.equal(404)

    def _post_schedule(self):
        body = VALID_SCHEDULES['schedule_with_empty_entries']['body']
        resp = self.app.post_json('/v1/tenant/schedules', body)
        require(resp.status_int).to.equal(201)
        require(resp.json).to.contain('schedule_id')
        return resp
