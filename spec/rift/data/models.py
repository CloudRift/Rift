from specter import Spec, expect
from rift.data.models.job import Job
from rift.data.models.target import Target
from rift.data.models.action import Action
from rift.data.models.tenant import Tenant
from uuid import uuid4


def create_target():
    source_dict = {
        "name": "Apache node 2",
        "type": "cloud-server",
        "address": {
            "nova": {
                "name": "apache-02.ord.dev",
                "region": "DFW"
                }
        },
        "authentication": {
            "rackspace": {
                "username": "your_username",
                "api_key": "your_api_key"
            }
        }
    }
    return Target.build_target_from_dict(str(uuid4()), source_dict)


class TestingDataModels(Spec):

    class JobModel(Spec):
        def can_convert_to_dictionary(self):
            target1 = create_target()
            target2 = create_target()
            targets = [target1, target2]

            actions = [
                Action(targets=targets, action_type="soft-reboot"),
                Action(targets=targets, action_type="apache-restart")
            ]

            job = Job(
                tenant_id="123",
                name="do_stuff",
                actions=actions,
                job_id="12345"
            )
            job_dict = job.as_dict()

            test_dict = Job.build_job_from_dict(job_dict).as_dict()
            expect(job_dict).to.equal(test_dict)

    class TargetModel(Spec):
        def can_convert_to_dictionary(self):
            target = create_target()
            target_dict = target.as_dict()

            tenant_id = str(uuid4())
            test_dict = Target.build_target_from_dict(
                tenant_id, target_dict).as_dict()
            expect(target_dict).to.equal(test_dict)

    class TenantModel(Spec):
        def can_convert_to_dictionary(self):
            tenant = Tenant(name=str(uuid4()), tenant_id=str(uuid4()))
            tenant_dict = tenant.as_dict()

            test_dict = Tenant.build_tenant_from_dict(tenant_dict).as_dict()
            expect(tenant_dict).to.equal(test_dict)

    class ActionModel(Spec):
        def can_convert_to_dictionary(self):
            target1 = create_target()
            target2 = create_target()
            targets = [target1, target2]
            action = Action(targets=targets, action_type="soft-reboot")
            action_dict = action.as_dict()

            test_dict = Action.build_action_from_dict(action_dict).as_dict()
            expect(action_dict).to.equal(test_dict)
