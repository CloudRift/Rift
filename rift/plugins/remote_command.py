"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from rift import log
from rift.api.worker.resources import ActionResource
from rift.clients.ssh import SSHClient, SSHKeyCredentials
from rift.data.models.target import Target
from rift.plugins import AbstractPlugin

LOG = log.get_logger()


class RemoteCommandPlugin(AbstractPlugin, ActionResource):

    def get_name(self):
        return 'remote-command'

    def execute_action(self, job, action):
        cmd = action.parameters.get('command')

        for target_id in action.targets:
            target = Target.get_target(job.tenant_id, target_id)
            ip = target.address.address_child
            ssh = target.authentication.get('ssh')

            creds = SSHKeyCredentials(
                username=ssh.get('username'),
                key_contents=ssh.get('private_key')
            )
            client = SSHClient(
                host=ip.address,
                port=ip.port,
                credentials=creds
            )
            client.connect()
            LOG.info('Remote command plugin executing: %s', cmd)
            resp = client.execute(command=cmd)
            client.close()
            LOG.info('Remote command plugin execution response: %s', resp)
