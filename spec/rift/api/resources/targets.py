import json

from specter import DataSpec, expect, fixture, require

from spec.rift.api.resources.fixtures import MockedDatabase
import spec.rift.api.schemas.target


class TargetsResource(MockedDatabase):

    def can_list_targets(self):
        resp = self.app.get('/v1/tenant/targets')
        require(resp.status_int).to.equal(200)
        require(resp.json).to.contain('targets')
        expect(resp.json['targets']).to.equal([])

    class SuccessfulPostRequests(MockedDatabase, DataSpec):
        DATASET = spec.rift.api.schemas.target.TargetValidator.ValidTarget.DATASET

        def can_post(self, body):
            resp = self.app.post_json('/v1/tenant/targets', body)
            require(resp.status_int).to.equal(201)
            expect(resp.json).to.contain('target_id')

    class BadPostRequests(MockedDatabase, DataSpec):
        DATASET = spec.rift.api.schemas.target.TargetValidator.InvalidTarget.DATASET

        def returns_400_on_a(self, body):
            resp = self.app.post_json('/v1/tenant/targets', body,
                                      expect_errors=True)
            expect(resp.status_int).to.equal(400)
