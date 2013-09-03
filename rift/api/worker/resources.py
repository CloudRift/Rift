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
from falcon import HTTP_200
from rift.api.common.resource import ApiResource
from rift.plugins import AbstractPlugin


class AvailableActionsResource(ApiResource):

    def __init__(self, action_plugins_list=[]):
        super(AvailableActionsResource, self).__init__()
        self.action_plugins = action_plugins_list

    def get_available_actions_dict(self, actions):
        action_names = [action.get_name() for action in actions
                        if issubclass(type(action), AbstractPlugin)]

        # Make sure we don't return duplicates
        action_names = list(set(action_names))

        body = {
            'available_actions': action_names
        }
        return body

    def on_get(self, req, resp):
        body = self.get_available_actions_dict(self.action_plugins)

        resp.status = HTTP_200
        resp.body = self.format_response_body(body)
