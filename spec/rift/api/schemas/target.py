from jsonschema.exceptions import ValidationError

from specter import Spec, DataSpec, expect
from rift.api.schemas import get_validator
from rift.api.schemas.target import target_schema
from spec.rift.api.datasets import INVALID_TARGETS, VALID_TARGETS


class TargetValidator(Spec):

    class InvalidTarget(DataSpec):
        DATASET = INVALID_TARGETS

        def fails_to_validate(self, body):
            validator = get_validator(target_schema)
            expect(validator.validate, [body]).to.raise_a(ValidationError)

    class ValidTarget(DataSpec):
        DATASET = VALID_TARGETS

        def validates(self, body):
            validator = get_validator(target_schema)
            validator.validate(body)
