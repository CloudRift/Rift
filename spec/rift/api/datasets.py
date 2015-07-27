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
        'body': """{
            "name": "a valid schedule with no entries",
            "entries": []
        }"""
    },
    'schedule_with_one_entry': {
        'body': """{
            "name": "a valid schedule with one entry",
            "entries": [
                {
                    "job_id": "5e48c156-7550-485d-bcdc-227c2c20d120",
                    "delay": 0
                }
            ]
        }"""
    },
    'schedule_with_two_entries': {
        'body': """{
            "name": "a valid schedule with two entries",
            "entries": [
                {
                    "job_id": "5e48c156-7550-485d-bcdc-227c2c20d120",
                    "delay": 0
                },
                {
                    "job_id": "f06f0ec2-bebf-492f-9a5e-1f8f18d5c277",
                    "delay": 10
                }
            ]
        }"""
    },
}

INVALID_SCHEDULES = {
    'schedule_with_missing_entries': {
        'body': """{
            "name": "a schedule missing the 'entries' key"
        }"""
    },
    'schedule_with_missing_name': {
        'body': """{
            "entries": []
        }"""
    },
    'schedule_without_delay': {
        'body': """{
            "name": "a schedule with a missing delay key",
            "entries": [
                {
                    "job_id": "f06f0ec2-bebf-492f-9a5e-1f8f18d5c277"
                }
            ]
        }"""
    },
    'schedule_with_negative_delay': {
        'body': """{
            "name": "a schedule with a missing delay key",
            "entries": [
                {
                    "job_id": "f06f0ec2-bebf-492f-9a5e-1f8f18d5c277"
                }
            ]
        }"""
    },
    'schedule_with_negative_delay': {
        'body': """{
            "name": "a schedule with a missing delay key",
            "entries": [
                {
                    "job_id": "f06f0ec2-bebf-492f-9a5e-1f8f18d5c277",
                    "delay": -1
                }
            ]
        }"""
    },
    'schedule_without_job_id': {
        'body': """{
            "name": "a schedule with a missing delay key",
            "entries": [
                {
                    "delay": -1
                }
            ]
        }"""
    },
    'schedule_with_wrong_delay_datatype': {
        'body': """{
            "name": "a schedule with a missing delay key",
            "entries": [
                {
                    "delay": "aaa"
                }
            ]
        }"""
    }
}
