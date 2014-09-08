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


class BaseClient(object):
    __meta__ = abc.ABCMeta

    def __init__(self, client=None, host=None, port=None, credentials=None):
        self.client = client
        self.host = host
        self.port = port
        self.credentials = credentials

    @abc.abstractmethod
    def connect(self, host=None, port=None, credentials=None):
        if host:
            self.host = host
        if port:
            self.port = port
        if credentials:
            self.credentials = credentials
