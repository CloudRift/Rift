"""
Copyright 2014 Rackspace

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
import abc
import paramiko
import six

from rift.clients import BaseClient


class SSHCredentials(object):
    __meta__ = abc.ABCMeta

    @abc.abstractmethod
    def get_paramiko_kwargs(self):
        raise NotImplementedError()  # pragma: no cover


class SSHKeyCredentials(SSHCredentials):

    def __init__(self, key_contents, username, password=None):
        self.contents = key_contents
        self.username = username
        self.password = password

    def get_paramiko_kwargs(self):
        return {
            'username': self.username,
            'pkey': self.paramiko_key
        }

    @property
    def paramiko_key(self):
        return paramiko.RSAKey.from_private_key(
            file_obj=six.StringIO(self.contents),
            password=self.password)


class SSHClient(BaseClient):

    def __init__(self, client=None, host=None, port=None, credentials=None):
        if not client:
            client = paramiko.SSHClient()
        super(SSHClient, self).__init__(client, host, port, credentials)

    def _set_key_policy(self, policy=None):
        if not policy:
            policy = paramiko.client.AutoAddPolicy()

        self.client.set_missing_host_key_policy(policy)

    def connect(self, host=None, port=None, credentials=None):
        super(SSHClient, self).connect(host, port, credentials)

        connect_kwargs = {
            'hostname': host or self.host,
            'port': port or self.port,
        }
        connect_kwargs.update(self.credentials.get_paramiko_kwargs())

        # Force auto add key policy
        self._set_key_policy()

        # Connect to Server
        self.client.connect(**connect_kwargs)

        return self

    def execute(self, command):
        stdin, stdout, stderr = self.client.exec_command(command, get_pty=True)
        return (stdout.readlines(), stderr.readlines())

    def close(self):
        self.client.close()
        return self
