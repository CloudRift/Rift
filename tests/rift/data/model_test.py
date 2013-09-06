import unittest
from rift.data import model


class WhenTestingDataModel(unittest.TestCase):

    def test_job_as_dict(self):
        targets = [
            model.Target(
                name="target1",
                public_ip="192.168.1.1",
                private_ip="127.0.0.1"
            ),
            model.Target(
                name="target2",
                public_ip="192.168.1.2",
                private_ip="127.0.0.1"
            )]
        actions = [
            model.Action(targets=targets, action_type="soft-reboot"),
            model.Action(targets=targets, action_type="apache-restart")
        ]
        job = model.Job(
            tenant_id="123",
            name="do_stuff",
            actions=actions,
            job_id="12345"
        )
        job_dict =  job.as_dict()

        test_job = model.build_job_from_dict(job_dict)
        self.assertEqual(job_dict, test_job.as_dict())

        model.save_job(test_job)
        job = model.get_job(test_job.job_id)
        print job.as_dict()

