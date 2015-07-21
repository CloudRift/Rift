from specter import Spec, expect
from pretend import stub, call_recorder, call
from mock import patch

from rift.data.models.target import Target
from rift.plugins.nova import NovaSoftReboot


class TestNovaSoftRebootPlugin(Spec):

    def before_each(self):
        self.plugin = NovaSoftReboot()
        self.job = stub(tenant_id='test_tenant')
        self.action = stub(targets=['d8659253-ce8e-48dc-9c93-495fa39fe7ad'])

    @patch('rift.plugins.nova.get_driver')
    @patch('rift.data.models.target.Target.get_target')
    def can_execute_action(self, get_target, get_driver):
        target = self.VALID_TARGET
        nodes = [
            stub(name="my.server.com", reboot=call_recorder(lambda: True)),
            stub(name="not.my.server.com", reboot=call_recorder(lambda: True)),
        ]
        driver_stub = self._get_libcloud_driver_stub(nodes)
        get_target.return_value = target
        get_driver.return_value = driver_stub

        self.plugin.execute_action(self.job, self.action)

        get_target.assert_called_with(
            self.job.tenant_id, self.action.targets[0])
        expect(driver_stub.calls).to.equal(
            [call('myusername', 'myapikey', region='dfw')])
        expect(len(nodes[0].reboot.calls)).to.equal(1)
        expect(len(nodes[1].reboot.calls)).to.equal(0)

    @patch('rift.plugins.nova.get_driver')
    @patch('rift.data.models.target.Target.get_target')
    def raises_exception_on_invalid_address(self, get_target, get_driver):
        target = self.TARGET_WITH_IP_ADDRESS
        driver_stub = self._get_libcloud_driver_stub([])
        get_target.return_value = target
        get_driver.return_value = driver_stub

        expect(self.plugin.execute_action, [self.job, self.action]) \
            .to.raise_a(Exception)

    @patch('rift.plugins.nova.get_driver')
    @patch('rift.data.models.target.Target.get_target')
    def raises_exception_on_unsupported_provider(self, get_target, get_driver):
        target = self.TARGET_WITH_UNSUPPORTED_PROVIDER
        driver_stub = self._get_libcloud_driver_stub([])
        get_target.return_value = target
        get_driver.return_value = driver_stub

        expect(self.plugin.execute_action, [self.job, self.action]) \
            .to.raise_a(Exception)

    def plugin_returns_a_name(self):
        expect(self.plugin.get_name()).to.equal('nova-soft-reboot')

    def _get_libcloud_driver_stub(self, nodes):
        libcloud_stub = stub(list_nodes=call_recorder(lambda: nodes))

        def driver_class(user, key, region):
            return libcloud_stub
        return call_recorder(driver_class)

    VALID_TARGET = Target.build_target_from_dict(
        'test_tenant',
        {
            "name": "a valid nova target with rax auth",
            "type": "cloud-server",
            "address": {
                "nova": {
                    "name": "my.server.com",
                    "region": "DFW",
                }
            },
            "authentication": {
                "rackspace": {
                    "username": "myusername",
                    "api_key": "myapikey"
                }
            },
        }
    )

    TARGET_WITH_IP_ADDRESS = Target.build_target_from_dict(
        'test_tenant',
        {
            "name": "a nova target with an ip address",
            "type": "cloud-server",
            "address": {
                "ip": {
                    "address": "127.0.0.1",
                    "port": 21,
                }
            },
            "authentication": {
                "rackspace": {
                    "username": "myusername",
                    "api_key": "myapikey"
                }
            },
        }
    )

    TARGET_WITH_UNSUPPORTED_PROVIDER = Target.build_target_from_dict(
        'test_tenant',
        {
            "name": "a nova target with invalid auth",
            "type": "cloud-server",
            "address": {
                "nova": {
                    "name": "my.server.com",
                    "region": "DFW",
                }
            },
            "authentication": {
                "azure": {
                    "username": "myusername",
                    "api_key": "myapikey"
                }
            },
        }
    )
