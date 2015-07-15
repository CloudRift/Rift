"""
Copyright 2013-2014 Rackspace

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
import uuid
import falcon
import json

from rift.api.common.resources import ApiResource
from rift.data.models.job import Job
from rift.data.models.tenant import Tenant
from rift.data.models.target import Target
from rift.actions import execute_job


class JobsResource(ApiResource):

    def on_post(self, req, resp, tenant_id):
        body = self.load_body(req)
        body['tenant_id'] = tenant_id

        job = Job.build_job_from_dict(body)
        Job.save_job(job)

        resp.status = falcon.HTTP_201
        resp.body = self.format_response_body({'job_id': job.id})

    def on_get(self, req, resp, tenant_id):
        jobs_list = [job.summary_dict() for job in Job.get_jobs(tenant_id)]
        resp.body = self.format_response_body({'jobs': jobs_list})


class JobResource(ApiResource):

    def on_get(self, req, resp, tenant_id, job_id):
        job = Job.get_job(job_id)
        if job:
            resp.body = self.format_response_body(job.as_dict())
        else:
            msg = 'Cannot find job: {job_id}'.format(job_id=job_id)
            resp.status = falcon.HTTP_404
            resp.body = json.dumps({'description': msg})

    def on_head(self, req, resp, tenant_id, job_id):
        job = Job.get_job(job_id)
        if job:
            # TODO(jmv): Figure out scheduling of jobs
            execute_job.delay(job.id)
            resp.status = falcon.HTTP_200
        else:
            msg = 'Cannot find job: {job_id}'.format(job_id=job_id)
            resp.status = falcon.HTTP_404
            resp.body = json.dumps({'description': msg})

    def on_delete(self, req, resp, tenant_id, job_id):
        Job.delete_job(job_id=job_id)


class TenantsResource(ApiResource):

    def on_post(self, req, resp, tenant_id):
        body = self.load_body(req)
        body['tenant_id'] = tenant_id

        tenant = Tenant.build_tenant_from_dict(body)
        Tenant.save_tenant(tenant)

        resp.status = falcon.HTTP_201
        resp.body = self.format_response_body({'tenant_id': tenant.id})

    def on_get(self, req, resp, tenant_id):
        tenant = Tenant.get_tenant(tenant_id)
        if tenant:
            resp.body = self.format_response_body(tenant.as_dict())
        else:
            msg = 'Cannot find tenant: {tenant_id}'.format(tenant_id=tenant_id)
            resp.status = falcon.HTTP_404
            resp.body = json.dumps({'description': msg})

    def on_put(self, req, resp, tenant_id):
        tenant = Tenant.get_tenant(tenant_id)
        if tenant:
            body = self.load_body(req)
            body['tenant_id'] = tenant_id

            tenant = Tenant.build_tenant_from_dict(body)
            Tenant.update_tenant(tenant)
        else:
            msg = 'Cannot find tenant: {tenant_id}'.format(tenant_id=tenant_id)
            resp.status = falcon.HTTP_404
            resp.body = json.dumps({'description': msg})


class TargetsResource(ApiResource):

    def on_post(self, req, resp, tenant_id):
        target_id = str(uuid.uuid4())

        body = self.load_body(req)
        body['id'] = target_id

        target = Target.build_target_from_dict(tenant_id, body)
        duplicate_target = Target.get_target(tenant_id, target_id=target.name)

        if duplicate_target:
            raise falcon.exceptions.HTTPConflict(
                'Duplicate Target Name',
                'Target names must be unique: {0}'.format(target.name))

        Target.save_target(target)

        resp.status = falcon.HTTP_201
        resp.body = self.format_response_body({'target_id': target_id})

    def on_get(self, req, resp, tenant_id):
        targets = Target.get_targets(tenant_id)
        target_list = [target.summary_dict() for target in targets]

        resp.body = self.format_response_body({'targets': target_list})


class TargetResource(ApiResource):

    def on_get(self, req, resp, tenant_id, target_id):
        target = Target.get_target(tenant_id, target_id)
        if target:
            resp.body = self.format_response_body(target.as_dict())
        else:
            msg = 'Cannot find target: {target_id}'.format(target_id=target_id)
            resp.status = falcon.HTTP_404
            resp.body = json.dumps({'description': msg})

    def on_delete(self, req, resp, tenant_id, target_id):
        Target.delete_target(target_id=target_id)
