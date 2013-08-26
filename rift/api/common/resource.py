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
from json import dumps as dict_to_str


class ApiResource(object):

    def format_response_body(self, body_dict):
        return dict_to_str(body_dict)

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_404

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_404