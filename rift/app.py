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

from rift.api.version.resources import VersionResource
from rift.api.resources import JobsResource, GetJobResource


class App(falcon.API):
    def __init__(self):
        super(App, self).__init__()

        version = VersionResource()
        jobs = JobsResource()
        get_job = GetJobResource()

        self.add_route('/', version)
        self.add_route('/v1/{tenant_id}/jobs', jobs)
        self.add_route('/v1/{tenant_id}/jobs/{job_id}', get_job)

application = App()
