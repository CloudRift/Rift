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
import json

from falcon import HTTP_200
from abc import ABCMeta, abstractmethod


class AbstractPlugin():
    __metaclass__ = ABCMeta
    API_HELP = """Add an API_HELP attribute to your plugin class to allow
users to better understand how they should use your plugin.
"""

    def on_get(self, req, resp):
        resp.status = HTTP_200
        resp.body = json.dumps({'help': self.API_HELP})

    @abstractmethod
    def get_name(self):
        return ''

    @abstractmethod
    def execute_action(self, action):
        pass

    # @abstractmethod
    # def on_post(self, req, resp):
    #    pass
