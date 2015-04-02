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

from rift import log
from rift.data import common
from rift.api.version.resources import VersionResource
from rift.api.resources import (JobsResource, JobResource, TenantsResource,
                                TargetsResource, TargetResource)

LOG = log.get_logger()


class App(falcon.API):
    def __init__(self):
        super(App, self).__init__()

        LOG.info('Starting Rift...')

        # Make sure we can load an encryption key
        common.get_secret_key()

        version = VersionResource()
        jobs = JobsResource()
        get_job = JobResource()
        tenants = TenantsResource()
        targets = TargetsResource()
        get_target = TargetResource()

        self.add_route('/', version)
        self.add_route('/v1/{tenant_id}', tenants)
        self.add_route('/v1/{tenant_id}/jobs', jobs)
        self.add_route('/v1/{tenant_id}/jobs/{job_id}', get_job)
        self.add_route('/v1/{tenant_id}/targets', targets)
        self.add_route('/v1/{tenant_id}/targets/{target_id}', get_target)

application = App()
