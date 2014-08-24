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
from rift.plugins import AbstractPlugin
from rift.api.worker.resources import ActionResource


class NovaSoftReboot(ActionResource, AbstractPlugin):
    API_HELP = """
    This plugin just requires a target and authentication.
    """

    def get_name(self):
        return 'nova-soft-reboot'

    def on_post(self, req, resp):
        super(NovaSoftReboot, self).on_post(req, resp)

    def execute_action(self, action):
        pass
