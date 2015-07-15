from jsonschema.exceptions import ValidationError

from specter import Spec, DataSpec, expect
from rift.api.schemas import get_validator
from rift.api.schemas.target import target_schema


class TargetValidator(Spec):

    class InvalidTarget(DataSpec):
        DATASET = {
            'target_with_empty_body': {
                'body': {}
            },
            'target_without_name': {
                'body': {
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
                            "api_key": "15a3b420df594067974dec1bd331c6c1"
                        }
                    }
                }
            },
            'target_without_address': {
                'body': {
                    "name": "a target without an address section",
                    "type": "cloud-server",
                    "authentication": {
                        "rackspace": {
                            "username": "myusername",
                            "api_key": "15a3b420df594067974dec1bd331c6c1"
                        }
                    }
                }
            },
            'target_without_authentication': {
                'body': {
                    "name": "a target without an authentication section",
                    "type": "cloud-server",
                    "address": {
                        "nova": {
                            "name": "my.server.com",
                            "region": "DFW",
                        }
                    }
                }
            },
            'target_with_invalid_nova_address': {
                'body': {
                    "name": "a target without an authentication section",
                    "type": "cloud-server",
                    "authentication": {
                        "rackspace": {
                            "username": "myusername",
                            "api_key": "15a3b420df594067974dec1bd331c6c1"
                        }
                    },
                    "address": {
                        "nova": {
                            "name": "my.server.com",
                            "password": "mypassword",
                        }
                    }
                }
            },
            'target_with_invalid_rax_auth': {
                'body': {
                    "name": "a target without an authentication section",
                    "type": "cloud-server",
                    "authentication": {
                        "rackspace": {
                            "badusernamekey": "myusername",
                            "api_key": "15a3b420df594067974dec1bd331c6c1"
                        }
                    },
                    "address": {
                        "nova": {
                            "name": "my.server.com",
                            "region": "DFW",
                        }
                    }
                }
            },
        }

        def fails_to_validate(self, body):
            validator = get_validator(target_schema)
            expect(validator.validate, [body]).to.raise_a(ValidationError)

    class ValidTarget(DataSpec):
        DATASET = {
            'nova_target_with_rax_auth': {
                'body': {
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
                            "api_key": "15a3b420df594067974dec1bd331c6c1"
                        }
                    },
                }
            },
            'ip_target_with_ssh_key_auth': {
                'body': {
                    "name": "a valid ip target with ssh key auth",
                    "type": "cloud-server",
                    "address": {
                        "ip": {
                            "address": "127.0.0.1",
                            "port": 21,
                        }
                    },
                    "authentication": {
                        "ssh": {
                            "username": "myusername",
                            "private_key": "-----BEGIN RSA PRIVATE KEY-----\n"
                                           "Proc-Type: 4,ENCRYPTED...",
                            "private_key_password": "15a3b420df594067974",
                        }
                    },
                }
            },
            'hostname_target_with_ssh_password_auth': {
                'body': {
                    "name": "a valid hostname target with ssh password auth",
                    "type": "cloud-server",
                    "address": {
                        "ip": {
                            "address": "127.0.0.1",
                            "port": 21,
                        }
                    },
                    "authentication": {
                        "ssh": {
                            "username": "myusername",
                            "password": "15a3b420df594067974dec1bd331c6c1",
                        }
                    },
                }
            }
        }

        def validates(self, body):
            validator = get_validator(target_schema)
            validator.validate(body)
