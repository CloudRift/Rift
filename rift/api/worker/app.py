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
import falcon

from rift.api.worker.resources import AvailableActionsResource
from rift.config import get_config
from rift import actions, task_queue

conf = get_config()


class WorkerApp(falcon.API):

    def __init__(self):
        super(WorkerApp, self).__init__()
        self.action_plugins = actions.ACTION_PLUGINS

        available_actions = AvailableActionsResource(self.action_plugins)
        self.add_route('/actions', available_actions)

        for action in self.action_plugins:
            route_name = '/actions/{name}'.format(name=action.get_name())
            self.add_route(route_name, action)


application = WorkerApp()
celery = task_queue.celery
