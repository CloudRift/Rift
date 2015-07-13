_action_schema = {
    "type": "object",
    "properties": {
        "targets": {
            "type": "array",
            "items": {"type": "string"},
        },
        "type": {
            "type": "string"
        },
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
            }
        }
    }
}

job_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "actions": {
            "type": "array",
            "items": _action_schema,
        }
    },
    "required": ["name", "actions"],
}
