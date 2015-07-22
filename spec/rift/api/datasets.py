# TODO(pglass): use plain dicts after specter fix for lists of dicts
INVALID_JOBS = {
    'job_with_empty_body': {
        'body': """{}"""
    },
    'job_without_name': {
        'body': """{
            "actions": []
        }"""
    },
    'job_without_actions': {
        'body': """{
            "name": "a job without any actions"
        }"""
    },
    'job_with_invalid_action': {
        'body': """{
            "name": "a job with an invalid action",
            "actions": [
                {
                    "targets": [],
                    "hello": "goodbye"
                }
            ]
        }"""
    }
}

# TODO(pglass): use plain dicts after specter fix for lists of dicts
VALID_JOBS = {
    'job_with_empty_actions': {
        'body': """{
            "name": "a job with no actions",
            "actions": []
        }"""
    },
    'job_with_empty_targets': {
        'body': """{
            "name": "a job with an action that has no targets",
            "actions": [
                {
                    "targets": [],
                    "type": "nova-soft-reboot"
                }
            ]
        }"""
    },
    'job_with_multiple_actions': {
        'body': """{
            "name": "a job with multiple different actions",
            "actions": [
                {
                    "targets": [
                        "c6b38cbf-9331-4495-b258-1a8fc71a3afc"
                    ],
                    "type": "nova-soft-reboot"
                },
                {
                    "targets": [
                        "c6b38cbf-9331-4495-b258-1a8fc71a3afc"
                    ],
                    "type": "remote-command",
                    "parameters": {
                        "command": "sudo service barbican-api restart"
                    }
                }
            ]
        }"""
    }
}

INVALID_TARGETS = {
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

VALID_TARGETS = {
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

VALID_SCHEDULES = {
    'schedule_with_empty_entries': {
        'body': {
            "name": "a valid schedule with no entries",
            "entries": [],
        }
    }
}
