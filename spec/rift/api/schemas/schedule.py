import json

from jsonschema.exceptions import ValidationError

from specter import Spec, DataSpec, expect
from rift.api.schemas import get_validator
from rift.api.schemas.schedule import schedule_schema
from spec.rift.api.datasets import INVALID_SCHEDULES, VALID_SCHEDULES


class ScheduleValidator(Spec):

    class InvalidSchedule(DataSpec):
        DATASET = INVALID_SCHEDULES

        def fails_to_falidate(self, body):
            body = json.loads(body)
            validator = get_validator(schedule_schema)
            expect(validator.validate, [body]).to.raise_a(ValidationError)

    class ValidSchedule(DataSpec):
        DATASET = VALID_SCHEDULES

        def validates(self, body):
            body = json.loads(body)
            validator = get_validator(schedule_schema)
            validator.validate(body)
