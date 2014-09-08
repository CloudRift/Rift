"""
Copyright 2014 Rackspace

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
from rift.plugins import AbstractPlugin
from rift.api.worker.resources import ActionResource
from rift.data.models.target import Target


class EchoPlugin(AbstractPlugin, ActionResource):
    API_HELP = """This plugin is just an example for plugin integration."""

    def get_name(self):
        return 'echo-sample'

    def on_post(self, req, resp):
        super(EchoPlugin, self).on_post(req, resp)

    def execute_action(self, job, action):
        # TODO: Replace with actual logging
        print('Executing a sample action')
        print('Tenant ID: {0}'.format(job.tenant_id))
        print('Target IDs: {0}'.format(action.targets))
        targets = [Target.get_target(job.tenant_id, target_id)
                   for target_id in action.targets]
        print('Targets: {0}'.format(targets))
        print('Type: {0}'.format(action.action_type))
        print('Params: {0}'.format(action.parameters))
