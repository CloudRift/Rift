import paramiko
from pretend import stub, call_recorder
from specter import Spec, expect

from rift.clients.ssh import SSHClient, SSHKeyCredentials
from spec.rift.clients import GARBAGE_PRIVATE_KEY_FOR_TEST


def create_paramiko_client_stub(connect_rtn=None, policy_rtn=None,
                                command_stdout_rtn=None, close_rtn=None,
                                command_stderr_rtn=None):

    stdout = stub(readlines=lambda: command_stdout_rtn)
    stderr = stub(readlines=lambda: command_stderr_rtn)

    connect = lambda **kwargs: connect_rtn
    close = lambda: close_rtn
    exec_command = lambda command, get_pty: (None,  stdout, stderr)
    set_missing_host_key_policy = lambda policy: policy_rtn

    client_stub = stub(
        connect=call_recorder(connect),
        close=call_recorder(close),
        exec_command=call_recorder(exec_command),
        set_missing_host_key_policy=call_recorder(set_missing_host_key_policy)
    )
    return client_stub


def create_key_creds():
    return SSHKeyCredentials(
        key_contents=GARBAGE_PRIVATE_KEY_FOR_TEST, username='tester')


class SSHCredentials(Spec):
    class KeyBased(Spec):
        def before_each(self):
            self.creds = create_key_creds()

        def create_instance(self):
            expect(self.creds).not_to.be_none()
            expect(self.creds.username).to.equal('tester')
            expect(self.creds.contents).to.equal(GARBAGE_PRIVATE_KEY_FOR_TEST)

        def can_generate_a_paramiko_key(self):
            key = self.creds.paramiko_key
            expect(type(key)).to.equal(paramiko.RSAKey)

        def can_generate_paramiko_kwargs(self):
            kwargs = self.creds.get_paramiko_kwargs()
            key = self.creds.paramiko_key

            expect(kwargs.get('username')).to.equal('tester')
            expect(kwargs.get('pkey')).to.equal(key)


class SSHClientVerification(Spec):
    def before_each(self):
        self.paramiko_stub = create_paramiko_client_stub(
            command_stdout_rtn=[
                'total 132',
                'drwxr-xr-x   2 root root  4096 Sep  2 13:36 bin'
            ]
        )
        self.ssh_credentials = create_key_creds()

        self.ssh_client = SSHClient(client=self.paramiko_stub,
                                    host='bam',
                                    port=21,
                                    credentials=self.ssh_credentials)

    def can_create_an_instance(self):
        expect(self.ssh_client).not_to.be_none()

    def unassigned_client_auto_creates_a_paramiko_client(self):
        inst = SSHClient(host='bam', port=21, credentials=self.ssh_credentials)
        expect(inst).not_to.be_none()
        expect(type(inst.client)).to.equal(paramiko.SSHClient)

    def sets_key_policy_on_client(self):

        self.ssh_client._set_key_policy()
        set_host_key_method = self.paramiko_stub.set_missing_host_key_policy
        expect(len(set_host_key_method.calls)).to.equal(1)

    def can_connect(self):
        self.ssh_client.connect()
        expect(len(self.paramiko_stub.connect.calls)).to.equal(1)

    def can_connect_with_args(self):
        self.ssh_client.connect(
            host='sample.host',
            port=80,
            credentials=self.ssh_credentials)

        expect(self.ssh_client.host).to.equal('sample.host')
        expect(self.ssh_client.port).to.equal(80)

    def can_close(self):
        self.ssh_client.close()
        expect(len(self.paramiko_stub.close.calls)).to.equal(1)

    def can_execute_a_command(self):
        result = self.ssh_client.execute('ls -l /')
        expect(len(result[0])).to.be_greater_than(1)
