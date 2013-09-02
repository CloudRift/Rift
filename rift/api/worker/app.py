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
from pynsive.plugin.manager import PluginManager
from pynsive import rlist_classes

from rift.app import App
from rift.plugins import AbstractPlugin
from rift.api.worker.resources import AvailableActionsResource


class WorkerApp(App):

    def __init__(self):
        super(WorkerApp, self).__init__()
        self.action_plugins = []
        self.initialize_plugin_manager()

        available_actions = AvailableActionsResource(self.action_plugins)
        self.add_route('/actions', available_actions)

        # Add routes for all of the plugins
        for action in self.action_plugins:
            route_name = '/actions/{name}'.format(name=action.get_name())
            self.add_route(route_name, action)

    def initialize_plugin_manager(self):
        self.plugin_manager = PluginManager()

        plugin_types = rlist_classes('rift.plugins', self.is_plugin)
        self.load_plugins(plugin_types)

    def load_plugins(self, plugin_types):
        for plugin_type in plugin_types:
            try:
                plugin = plugin_type()
                self.action_plugins.append(plugin)
            except TypeError as error:
                print 'Could not load plugin: {type}\n * {error}'.format(
                    type=plugin_type, error=error)

    def is_plugin(self, type):
        return issubclass(type, AbstractPlugin) and type is not AbstractPlugin


application = WorkerApp()
