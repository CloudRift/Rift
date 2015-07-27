_entry_schema = {
    "additionalProperties": False,
    "properties": {
        "job_id": {"type": "string"},
        "delay": {
            "type": "integer",
            "minimum": 0
        },
    },
    "required": ["job_id", "delay"],
}

schedule_schema = {
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string"},
        "entries": {
            "type": "array",
            "items": _entry_schema,
        }
    },
    "required": ["name", "entries"],
}
