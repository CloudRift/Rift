from webtest import TestApp
from specter import Spec, expect, require

import rift.app


class VersionResource(Spec):

    def before_all(self):
        self.app = TestApp(rift.app.application)

    def can_get_version(self):
        resp = self.app.get('/')
        require(resp.json).to.contain('versions')
        require(resp.json['versions']).to.contain('v1')
        expect(resp.json['versions']['v1']).to.contain('status')
        expect(resp.json['versions']['v1']).to.contain('build')
