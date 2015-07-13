import jsonschema


def get_validator(schema):
    # the validator class is for the meta schema, if it's defined in the schema
    validator_class = jsonschema.validators.validator_for(schema)
    return validator_class(schema)
