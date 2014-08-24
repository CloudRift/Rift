from specter import Spec, expect
from rift.data.models.job import Job
from rift.data.models.action import Action
from spec.rift.data.common import create_target


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
