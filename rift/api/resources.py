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
from rift.api.common.resources import ApiResource
from rift.data.model import build_job_from_dict


class JobsResource(ApiResource):

    def on_post(self, req, resp, tenant_id):
        body = self.load_body(req)
        job = build_job_from_dict(body)

    def on_get(self, req, resp, tenant_id):
        pass
