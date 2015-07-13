"""
{
    "name": "Apache node 2",
    "type": "cloud-server",
    "address": {
        "nova": {
            "name": "apache-02.ord.dev",
            "region": "DFW"
            }
        },
    "authentication": {
        "rackspace": {
            "username": "your_username",
            "api_key": "your_api_key"
            }
        }
}
"""

_ip_schema = {
    "type": "object",
    "properties": {
        "ip": {
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "port": {"type": "integer"},
            }
        }
    }
}

_hostname_schema = {
    "type": "object",
    "properties": {
        "hostname": {
            "type": "object",
            "properties": {
                "address": {"type": "string"},
                "port": {"type": "integer"},
            }
        }
    }
}

_nova_schema = {
    "type": "object",
    "properties": {
        "nova": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "region": {"type": "string"},
            }
        }
    }
}

_rax_auth_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "api_key": {"type": "string"},
    }
}

_ssh_key_auth_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "private_key": {"type": "string"},
        "private_key_password": {"type": "string"},
    }
}

_ssh_password_auth_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
    }
}

target_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "type": {"type": "string"},
        "address": {
            "type": "object",
            "oneOf": [
                _ip_schema,
                _hostname_schema,
                _nova_schema,
            ]
        },
        "authentication": {
            "type": "object",
            "oneOf": [
                _rax_auth_schema,
                _ssh_key_auth_schema,
                _ssh_password_auth_schema,
            ]
        }
    },
    "required": ["name", "type", "address", "authentication"]
}
