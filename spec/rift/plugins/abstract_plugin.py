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
from spec import Spec
from falcon import HTTP_200, Response
from rift.plugins import AbstractPlugin


class GenericPlugin(AbstractPlugin):

    def get_name(self):
        return 'generic'

    def on_post(self, req, resp):
        pass


class TestAbstractPlugin(Spec):

    def it_cannot_be_instantiated(self):
        try:
            result = AbstractPlugin()
        except TypeError:
            # Expected
            result = None
        assert result is None

    def it_should_allow_a_basic_implementation(self):
        plugin = GenericPlugin()
        assert issubclass(type(plugin), AbstractPlugin)

    def it_should_have_a_default_get_method(self):
        plugin = GenericPlugin()
        resp, req = Response(), object()

        plugin.on_get(req=req, resp=resp)
        assert resp.status == HTTP_200
        assert resp.body == AbstractPlugin.API_HELP
