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
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from rift import log
from rift.plugins import AbstractPlugin
from rift.api.worker.resources import ActionResource
from rift.data.models.address import NovaAddress
from rift.data.models.target import Target

LOG = log.get_logger()


class NovaSoftReboot(AbstractPlugin, ActionResource):
    API_HELP = """This plugin just requires a target and authentication."""

    def get_name(self):
        return 'nova-soft-reboot'

    def on_post(self, req, resp):
        super(NovaSoftReboot, self).on_post(req, resp)

    def execute_action(self, job, action):
        for target_id in action.targets:
            target = Target.get_target(job.tenant_id, target_id)
            self._reboot_target(target)

    def _reboot_target(self, target):
        address = target.address.address_child
        if not isinstance(address, NovaAddress):
            raise Exception("Nova soft reboot plugin requires a nova address")

        auth = target.authentication
        if 'rackspace' in auth:
            cls = get_driver(Provider.RACKSPACE)
            driver = cls(auth['rackspace']['username'],
                         auth['rackspace']['api_key'],
                         region=address.region.lower())
            nodes = [n for n in driver.list_nodes() if n.name == address.name]
        else:
            raise Exception("No supported providers in target: {0}"
                            .format(target.as_dict()))

        for node in nodes:
            LOG.info('Nova soft reboot plugin is rebooting %s', node.name)
            node.reboot()
