import json

from jsonschema.exceptions import ValidationError
from specter import Spec, DataSpec, expect

from rift.api.schemas import get_validator
from rift.api.schemas.job import job_schema
from spec.rift.api.datasets import INVALID_JOBS, VALID_JOBS


class JobValidator(Spec):

    class InvalidJob(DataSpec):
        DATASET = INVALID_JOBS

        def fails_to_validate(self, body):
            body = json.loads(body)
            validator = get_validator(job_schema)
            expect(validator.validate, [body]).to.raise_a(ValidationError)

    class ValidJob(DataSpec):
        DATASET = VALID_JOBS

        def validates(self, body):
            body = json.loads(body)
            validator = get_validator(job_schema)
            validator.validate(body)
