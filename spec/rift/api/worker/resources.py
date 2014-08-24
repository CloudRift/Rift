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
from specter import Spec, expect
from rift.api.worker.resources import AvailableActionsResource
from rift.plugins.nova import NovaSoftReboot


class AvailableActions(Spec):
    """ Get Available Actions Dictionary"""

    def before_each(self):
        self.plugins = [NovaSoftReboot()]
        self.resource = AvailableActionsResource()

    def _check_for_one_element(self, body):
        available_actions = body.get('available_actions')

        expect(available_actions).not_to.be_none()
        expect(len(available_actions)).to.equal(1)
        expect(available_actions[0]).to.equal('nova-soft-reboot')

    def should_handle_a_list_with_a_valid_plugin(self):
        body = self.resource.get_available_actions_dict(self.plugins)
        self._check_for_one_element(body)

    def should_not_contain_duplicates(self):
        bad_list = [NovaSoftReboot(), NovaSoftReboot()]
        body = self.resource.get_available_actions_dict(bad_list)

        self._check_for_one_element(body)

    def should_not_contain_non_plugin_types(self):
        bad_list = [NovaSoftReboot(), 'bam']
        body = self.resource.get_available_actions_dict(bad_list)

        self._check_for_one_element(body)
