import json

from jsonschema.exceptions import ValidationError

from specter import Spec, DataSpec, expect
from rift.api.schemas import get_validator
from rift.api.schemas.job import job_schema


class JobValidator(Spec):

    class InvalidJob(DataSpec):
        # TODO(pglass): use plain dicts after specter fix for lists of dicts
        DATASET = {
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

        def fails_to_validate(self, body):
            body = json.loads(body)
            validator = get_validator(job_schema)
            expect(validator.validate, [body]).to.raise_a(ValidationError)

    class ValidJob(DataSpec):
        # TODO(pglass): use plain dicts after specter fix for lists of dicts
        DATASET = {
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

        def validates(self, body):
            body = json.loads(body)
            validator = get_validator(job_schema)
            validator.validate(body)
