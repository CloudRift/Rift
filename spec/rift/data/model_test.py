from specter import Spec, expect
from rift.data.model import Job, Target, Action, Tenant
from uuid import uuid4


class TestingDataModel(Spec):

    def _create_target(self):
        return Target(name=str(uuid4()), type="cloud-server",
                      address={"ipv4": "4", "ipv6": "6"},
                      address_type="nova-name",
                      authentication={
                          "cloud_account": {
                              "username": "your_username",
                              "token": "your_api_token"
                          }
                      })

    def job_can_convert_to_dictionary(self):
        target1 = self._create_target()
        target2 = self._create_target()
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

        test_job = Job.build_job_from_dict(job_dict)
        expect(job_dict).to.equal(test_job.as_dict())

    def target_can_convert_to_dictionary(self):
        target = self._create_target()
        target_dict = target.as_dict()

        test_target = Target.build_target_from_dict(target_dict)
        expect(target_dict).to.equal(test_target.as_dict())

    def tenant_can_convert_to_dictionary(self):
        target1 = self._create_target()
        target2 = self._create_target()
        targets = [target1, target2]
        tenant = Tenant(name=str(uuid4()), tenant_id=str(uuid4()),
                        targets=targets)
        tenant_dict = tenant.as_dict()

        test_tenant = Tenant.build_tenant_from_dict(tenant_dict)
        expect(tenant_dict).to.equal(test_tenant.as_dict())

    def action_can_convert_to_dictionary(self):
        target1 = self._create_target()
        target2 = self._create_target()
        targets = [target1, target2]
        action = Action(targets=targets, action_type="soft-reboot")
        action_dict = action.as_dict()

        test_action = Action.build_action_from_dict(action_dict)
        expect(action_dict).to.equal(test_action.as_dict())
