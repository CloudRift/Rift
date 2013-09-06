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

from rift import task_queue
from rift.plugins import AbstractPlugin
from rift.data.model import get_job


def get_action_plugin(action_plugins, name):
    for action_plugin in action_plugins:
        if action_plugin.get_name() == name:
            return action_plugin


def load_plugins():

    plugin_manager = PluginManager()

    plugin_types = rlist_classes('rift.plugins', is_plugin)
    plugins = []
    for plugin_type in plugin_types:
        try:
            plugin = plugin_type()
            plugins.append(plugin)
        except TypeError as error:
            print 'Could not load plugin: {type}\n * {error}'.format(
                type=plugin_type, error=error)
    return plugins


def is_plugin(plugin_type):
    return (issubclass(
        plugin_type, AbstractPlugin)
            and plugin_type is not AbstractPlugin)


ACTION_PLUGINS = load_plugins()

@task_queue.celery.task
def execute_job(job_id):
    job = get_job(job_id)
    if not job:
        return

    for action in job.actions:
        plugin = get_action_plugin(ACTION_PLUGINS, action.action_type)

        if plugin:
            plugin.execute_action(action)
        else:
            print 'Failed to execute action: ', action.action_type
