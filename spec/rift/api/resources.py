from specter import Spec, expect, require
from webtest import TestApp

import rift.app
import rift.data.adapters.mongodb
import rift.data.handler


class JobsResource(Spec):

    def before_each(self):
        # reset the mocked DB to clear out any data it has
        rift.data.handler._db_handler = rift.data.adapters.mongodb.MongoDB()
        rift.data.handler._db_handler.connect()
        self.app = TestApp(rift.app.application)

    def can_list_jobs(self):
        # reuse another test case to post a job
        self.can_post_nova_reboot_job()

        resp = self.app.get('/v1/tenant/jobs')
        require(resp.json).to.contain('jobs')
        require(resp.json['jobs']).to.be_a(list)
        expect(len(resp.json['jobs'])).to.equal(1)

    def can_post_nova_reboot_job(self):
        resp = self.app.post_json('/v1/tenant/jobs', {
            "name": "a soft reboot job",
            "actions": [{
                "targets": ["83a57a53-4a50-42e5-acb4-dc301736062a"],
                "type": "nova-soft-reboot",
            }]
        })
        require(resp.status_int).to.equal(201)
        expect(resp.json).to.contain('job_id')

    def can_post_remote_command_job(self):
        resp = self.app.post_json('/v1/tenant/jobs', {
            "name": "a remote command job",
            "actions": [{
                "targets": ["83a57a53-4a50-42e5-acb4-dc301736062a"],
                "type": "remote-command",
                "parameters": {
                    "command": "sudo service barbican-api restart"
                }
            }]
        })
        require(resp.status_int).to.equal(201)
        expect(resp.json).to.contain('job_id')
