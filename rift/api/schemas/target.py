_ip_schema = {
    "additionalProperties": False,
    "properties": {
        "ip": {
            "additionalProperties": False,
            "properties": {
                "address": {"type": "string"},
                "port": {"type": "integer"},
            },
            "required": ["address", "port"],
        }
    }
}

_hostname_schema = {
    "additionalProperties": False,
    "properties": {
        "hostname": {
            "additionalProperties": False,
            "properties": {
                "address": {"type": "string"},
                "port": {"type": "integer"},
            },
            "required": ["address", "port"],
        }
    }
}

_nova_schema = {
    "additionalProperties": False,
    "properties": {
        "nova": {
            "additionalProperties": False,
            "properties": {
                "name": {"type": "string"},
                "region": {"type": "string"},
            },
            "required": ["name", "region"],
        }
    }
}

_rax_auth_schema = {
    "additionalProperties": False,
    "properties": {
        "rackspace": {
            "additionalProperties": False,
            "properties": {
                "username": {"type": "string"},
                "api_key": {"type": "string"},
            },
            "required": ["username", "api_key"],
        }
    }
}

_ssh_key_auth_schema = {
    "additionalProperties": False,
    "properties": {
        "ssh": {
            "additionalProperties": False,
            "properties": {
                "username": {"type": "string"},
                "private_key": {"type": "string"},
                "private_key_password": {"type": "string"},
            },
            "required": ["username", "private_key"],
        }
    }
}

_ssh_password_auth_schema = {
    "additionalProperties": False,
    "properties": {
        "ssh": {
            "additionalProperties": False,
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["username", "password"],
        }
    }
}

target_schema = {
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string"},
        "type": {"type": "string"},
        "address": {
            "oneOf": [
                _ip_schema,
                _hostname_schema,
                _nova_schema,
            ]
        },
        "authentication": {
            "oneOf": [
                _rax_auth_schema,
                _ssh_key_auth_schema,
                _ssh_password_auth_schema,
            ]
        }
    },
    "required": ["name", "type", "address", "authentication"]
}
