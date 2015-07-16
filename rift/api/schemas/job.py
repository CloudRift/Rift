_action_schema = {
    "additionalProperties": False,
    "properties": {
        "targets": {
            "type": "array",
            "items": {"type": "string"},
        },
        "type": {
            "type": "string"
        },
        "parameters": {
            "properties": {
                "command": {"type": "string"},
            }
        },
    },
    "required": ["targets", "type"],
}

job_schema = {
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string"},
        "actions": {
            "type": "array",
            "items": _action_schema,
        }
    },
    "required": ["name", "actions"],
}
