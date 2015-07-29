_entry_schema = {
    "additionalProperties": False,
    "properties": {
        "job_id": {"type": "string"},
        "delay": {
            "type": "string",
            "pattern": "[0-9]{2}:[0-9]{2}:[0-9]{2}",
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
