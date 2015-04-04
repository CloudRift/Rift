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


class ServicePlugin(AbstractPlugin, ActionResource):

    def get_name(self):
        return 'service'

    def _build_command(self, service_name, service_action):
        if service_action == 'pkill':
            cmd = 'sudo pkill {service_name}'.format(service_name=service_name)
        else:
            cmd = 'sudo service {service_name} {action} '.format(
                service_name=service_name,
                action=service_action
            )
        return cmd

    def execute_action(self, job, action):
        service_name = action.parameters.get('service-name')
        service_action = action.parameters.get('action')

        cmd = self._build_command(service_name, service_action)

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
            client.execute(command=cmd)
            client.close()
            LOG.info('Service plugin execution successful: %s', cmd)
