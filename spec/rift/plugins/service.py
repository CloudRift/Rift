from mock import patch
from pretend import stub
from specter import Spec, expect

from spec.rift.clients import GARBAGE_PRIVATE_KEY_FOR_TEST
from spec.rift.clients.ssh import create_paramiko_client_stub
from rift.data.models.action import Action
from rift.data.models.target import Target
from rift.plugins import service


class TestServicePlugin(Spec):

    def before_each(self):
        self.plugin = service.ServicePlugin()
        self.job = stub(tenant_id=lambda: 'test_tenant')
        self.paramiko_stub = create_paramiko_client_stub()
        self.target = Target.build_target_from_dict(
            'test_tenant',
            {
                'id': 'test_id',
                'type': 'something',
                'address': {
                    'ip': {
                        'address': '10.0.0.1',
                        'port': 21
                    }
                },
                'authentication': {
                    'ssh': {
                        'username': 'tester',
                        'private_key': GARBAGE_PRIVATE_KEY_FOR_TEST,
                    }
                },
                'name': 'test_target'
            }
        )

    @patch('paramiko.SSHClient')
    def can_pkill_a_process(self, ssh_client):
        ssh_client.return_value = self.paramiko_stub

        action = Action(
            targets=['test_id'],
            action_type='service',
            parameters={
                'service-name': 'nothing',
                'action': 'pkill'
            }
        )

        with patch('rift.data.models.target.Target.get_target') as g:
            g.return_value = self.target
            self.plugin.execute_action(self.job, action)

        expect(len(self.paramiko_stub.connect.calls)).to.equal(1)
        expect(len(self.paramiko_stub.exec_command.calls)).to.equal(1)
        expect(len(self.paramiko_stub.close.calls)).to.equal(1)

    @patch('paramiko.SSHClient')
    def can_stop_a_service(self, ssh_client):
        ssh_client.return_value = self.paramiko_stub

        action = Action(
            targets=['test_id'],
            action_type='service',
            parameters={
                'service-name': 'nothing',
                'action': 'stop'
            }
        )

        with patch('rift.data.models.target.Target.get_target') as g:
            g.return_value = self.target
            self.plugin.execute_action(self.job, action)

        expect(len(self.paramiko_stub.connect.calls)).to.equal(1)
        expect(len(self.paramiko_stub.exec_command.calls)).to.equal(1)
        expect(len(self.paramiko_stub.close.calls)).to.equal(1)

    def plugin_returns_a_name(self):
        expect(self.plugin.get_name()).to.equal('service')
